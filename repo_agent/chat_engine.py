import os, json
import time
import sys
import tiktoken
import inspect
from repo_agent.config import (
    language_mapping, 
    max_input_tokens_map, 
    max_output_token, 
    boundary_token
)
from repo_agent.prompt import SYS_PROMPT, USR_PROMPT
from repo_agent.doc_meta_info import DocItem
from collections import defaultdict
from repo_agent.log import logger
from typing import Dict, Literal
from openai import OpenAI, APIConnectionError


class ContextLengthExceededError(Exception):
    """Exception raised when the input size exceeds the model's context length limit."""
    pass

def get_relative_items_from_key(dictionary: Dict, target_key: str, direction: Literal["before", "after"]='after') -> Dict[str, int]:
    """
    获取与指定键相对位置的所有键值对。

    Args:
        dictionary (dict): 要操作的字典对象。
        target_key (str): 用于定位的键。
        direction (str, optional): 指定获取方向，'before'表示获取目标键之前的键值对，
                                   'after'表示获取目标键之后的键值对。默认为'after'。

    Returns:
        dict: 根据指定方向，相对于指定键的所有键值对构成的字典。

    Raises:
        ValueError: 如果方向参数不是'before'或'after'。
    """
    keys = list(dictionary.keys())
    try:
        key_index = keys.index(target_key)
    except ValueError:
        # 如果指定的键不在字典中，返回空字典
        return {}

    if direction == 'before':
        # 获取键之前的所有键值对
        selected_items = dict(list(dictionary.items())[:key_index])
    elif direction == 'after':
        # 获取键之后以及键的所有键值对
        selected_items = dict(list(dictionary.items())[key_index:])
    else:
        raise ValueError("Direction must be 'before' or 'after'.")

    return selected_items

def find_first_model_exceeding_limit(model_limits: Dict[str, int], minimum_tokens: int) -> str | None:
    """
    在给定的模型及其限制中，找到第一个输入限制超过指定数量的模型。

    Args:
        model_limits (dict): 模型及其对应的输入限制的字典。
        minimum_tokens (int): 指定的最小输入令牌数量。

    Returns:
        str: 第一个输入限制超过指定数量的模型名称。如果没有找到符合条件的模型，则返回None。
    """
    for model_name, token_limit in model_limits.items():
        if token_limit >= minimum_tokens:
            return model_name  # 返回第一个符合条件的模型名称
    return None  # 如果没有找到符合条件的模型，则返回None


def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [
        line
        for line in source_lines
        if line.strip().startswith("import") or line.strip().startswith("from")
    ]
    return import_lines


def build_path_tree(who_reference_me, reference_who, doc_item_path):
    def tree():
        return defaultdict(tree)

    path_tree = tree()

    for path_list in [who_reference_me, reference_who]:
        for path in path_list:
            parts = path.split(os.sep)
            node = path_tree
            for part in parts:
                node = node[part]

    # 处理 doc_item_path
    parts = doc_item_path.split(os.sep)
    parts[-1] = "✳️" + parts[-1]  # 在最后一个对象前面加上星号
    node = path_tree
    for part in parts:
        node = node[part]

    def tree_to_string(tree, indent=0):
        s = ""
        for key, value in sorted(tree.items()):
            s += "    " * indent + key + "\n"
            if isinstance(value, dict):
                s += tree_to_string(value, indent + 1)
        return s

    return tree_to_string(path_tree)


class ChatEngine:
    """
    ChatEngine is used to generate the doc of functions or classes.
    """

    def __init__(self, CONFIG):
        self.config = CONFIG

    def num_tokens_from_string(self, string: str, encoding_name="cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def generate_doc(self, doc_item: DocItem, file_handler):
        code_info = doc_item.content
        referenced = len(doc_item.who_reference_me) > 0

        code_type = code_info["type"]
        code_name = code_info["name"]
        code_content = code_info["code_content"]
        have_return = code_info["have_return"]
        who_reference_me = doc_item.who_reference_me_name_list
        reference_who = doc_item.reference_who_name_list
        file_path = doc_item.get_full_name()
        doc_item_path = file_path + "/" + code_name

        # 树结构路径通过全局信息中的who reference me 和 reference who + 自身的file_path来获取
        project_structure = build_path_tree(
            who_reference_me, reference_who, doc_item_path
        )

        # project_manager = ProjectManager(repo_path=file_handler.repo_path, project_hierarchy=file_handler.project_hierarchy)
        # project_structure = project_manager.get_project_structure()
        # file_path = os.path.join(file_handler.repo_path, file_handler.file_path)
        # code_from_referencer = get_code_from_json(project_manager.project_hierarchy, referencer) #
        # referenced = True if len(code_from_referencer) > 0 else False
        # referencer_content = '\n'.join([f'File_Path:{file_path}\n' + '\n'.join([f'Corresponding code as follows:\n{code}\n[End of this part of code]' for code in codes]) + f'\n[End of {file_path}]' for file_path, codes in code_from_referencer.items()])

        def get_referenced_prompt(doc_item: DocItem) -> str:
            if len(doc_item.reference_who) == 0:
                return ""
            prompt = [
                """As you can see, the code calls the following objects, their code and docs are as following:"""
            ]
            for k, reference_item in enumerate(doc_item.reference_who):
                instance_prompt = (
                    f"""obj: {reference_item.get_full_name()}\nDocument: \n{reference_item.md_content[-1] if len(reference_item.md_content) > 0 else 'None'}\nRaw code:```\n{reference_item.content['code_content'] if 'code_content' in reference_item.content.keys() else ''}\n```"""
                    + "=" * 10
                )
                prompt.append(instance_prompt)
            return "\n".join(prompt)

        def get_referencer_prompt(doc_item: DocItem) -> str:
            if len(doc_item.who_reference_me) == 0:
                return ""
            prompt = [
                """Also, the code has been called by the following objects, their code and docs are as following:"""
            ]
            for k, referencer_item in enumerate(doc_item.who_reference_me):
                instance_prompt = (
                    f"""obj: {referencer_item.get_full_name()}\nDocument: \n{referencer_item.md_content[-1] if len(referencer_item.md_content) > 0 else 'None'}\nRaw code:```\n{referencer_item.content['code_content'] if 'code_content' in referencer_item.content.keys() else 'None'}\n```"""
                    + "=" * 10
                )
                prompt.append(instance_prompt)
            return "\n".join(prompt)

        def get_relationship_description(referencer_content, reference_letter):
            if referencer_content and reference_letter:
                has_relationship = "And please include the reference relationship with its callers and callees in the project from a functional perspective"
            elif referencer_content:
                return "And please include the relationship with its callers in the project from a functional perspective."
            elif reference_letter:
                return "And please include the relationship with its callees in the project from a functional perspective."
            else:
                return ""

        
        max_tokens = self.config.get("max_document_tokens", 1024) or 1024
        max_attempts = 5  # 设置最大尝试次数
        language = self.config["language"] # setting document language
        if language not in language_mapping:
            raise KeyError(
                f"Language code {language} is not provided! Supported languages are: {json.dumps(language_mapping)}"
            )
        language = language_mapping[language]

        code_type_tell = "Class" if code_type == "ClassDef" else "Function"
        parameters_or_attribute = (
            "attributes" if code_type == "ClassDef" else "parameters"
        )
        have_return_tell = (
            "**Output Example**: Mock up a possible appearance of the code's return value."
            if have_return
            else ""
        )
        # reference_letter = "This object is called in the following files, the file paths and corresponding calling parts of the code are as follows:" if referenced else ""
        combine_ref_situation = (
            "and combine it with its calling situation in the project,"
            if referenced
            else ""
        )

        referencer_content = get_referencer_prompt(doc_item)
        reference_letter = get_referenced_prompt(doc_item)
        has_relationship = get_relationship_description(referencer_content, reference_letter)

        project_structure_prefix = ", and the related hierarchical structure of this project is as follows (The current object is marked with an *):"

        sys_prompt = SYS_PROMPT.format(
            combine_ref_situation=combine_ref_situation,
            file_path=file_path,
            project_structure_prefix=project_structure_prefix,
            project_structure=project_structure,
            code_type_tell=code_type_tell,
            code_name=code_name,
            code_content=code_content,
            have_return_tell=have_return_tell,
            # referenced=referenced,
            has_relationship=has_relationship,
            reference_letter=reference_letter,
            referencer_content=referencer_content,
            parameters_or_attribute=parameters_or_attribute,
            language=language,
        )

        usr_prompt = USR_PROMPT.format(language=language)

        # # 保存prompt到txt文件
        # with open(f'prompt_output/sys_prompt_{code_name}.txt', 'w', encoding='utf-8') as f:
        #     f.write(sys_prompt+'\n'+ usr_prompt)

        model = self.config["default_completion_kwargs"]["model"]
        max_input_tokens = max_input_tokens_map.get(model, 4096) - max_output_token - boundary_token

        input_tokens = (
            self.num_tokens_from_string(sys_prompt) +
            self.num_tokens_from_string(usr_prompt)
        )

        # 如果总tokens超过当前模型的限制，则尝试寻找较大模型或者缩减输入
        if input_tokens > max_input_tokens:
            # 查找一个拥有更大输入限制的模型
            first_larger_model = find_first_model_exceeding_limit(max_input_tokens_map, input_tokens)
            if first_larger_model is not None:
                # 选择一个拥有更大输入限制的模型
                model = first_larger_model
                logger.info(f"Use {model} for processing.")
            else:
                trim_max_retry = 2
                for attempt in range(trim_max_retry):
                    logger.info(f"Attempt {attempt + 1} of {trim_max_retry}: Reducing the length of the messages.")
                    if attempt == 0:
                        logger.info(f"Removed project_structure and project_structure_prefix to suit context window")
                        # 第一次尝试，移除 project_structure 和 project_structure_prefix
                        project_structure = ""
                        project_structure_prefix = ""
                    elif attempt == 1:
                        logger.info(f"Removed referencer_content, reference_letter, combine_ref_situation to suit context window")
                        # 第二次尝试，移除相关的调用者和被调用者信息
                        referenced = False
                        referencer_content = ""
                        reference_letter = ""
                        combine_ref_situation = ""
                        
                    # 更新 sys_prompt
                    sys_prompt = SYS_PROMPT.format(
                        reference_letter=reference_letter,
                        combine_ref_situation=combine_ref_situation,
                        file_path=file_path,
                        project_structure_prefix=project_structure_prefix,
                        project_structure=project_structure,
                        code_type_tell=code_type_tell,
                        code_name=code_name,
                        code_content=code_content,
                        have_return_tell=have_return_tell,
                        has_relationship=has_relationship,
                        referenced=referenced,
                        referencer_content=referencer_content,
                        parameters_or_attribute=parameters_or_attribute,
                        language=language,
                    )
                    
                    # 重新计算 tokens
                    total_tokens = (
                        self.num_tokens_from_string(sys_prompt) +
                        self.num_tokens_from_string(usr_prompt)
                    )
                    # 检查是否满足要求
                    if total_tokens <= max_input_tokens:
                        break
                    
                if total_tokens > max_input_tokens:
                    error_message = (
                        f"Context length of {total_tokens} exceeds the maximum limit of {max_input_tokens} tokens "
                        f"after {trim_max_retry} attempts."
                    )
                    # raise ContextLengthExceededError(error_message)
                    return None

        max_attempts = 5
        attempt = 0
        fallback_model = get_relative_items_from_key(max_input_tokens_map, model, 'after')
        for model, _ in fallback_model.items():
            while attempt < max_attempts:
                try:
                    # 获取基本配置
                    client = OpenAI(
                        api_key=self.config["api_keys"][model][0]["api_key"],
                        base_url=self.config["api_keys"][model][0]["base_url"],
                        timeout=self.config["default_completion_kwargs"]["request_timeout"],
                    )

                    messages = [
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": usr_prompt},
                    ]

                    response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=self.config["default_completion_kwargs"]["temperature"],
                        max_tokens=max_output_token,
                    )

                    response_message = response.choices[0].message

                    # 如果 response_message 是 None，则继续下一次循环
                    if response_message is None:
                        attempt += 1
                        continue
                    return response_message

                except APIConnectionError as e:
                    logger.error(f"Connection error: {e}. Attempt {attempt + 1} of {max_attempts}")
                    # Retry after 7 seconds
                    time.sleep(7)
                    attempt += 1
                    if attempt == max_attempts:
                        raise
                    else:
                        continue  # Try to request again
                except Exception as e:
                    logger.error(
                        f"An unknown error occurred: {e}. \nAttempt {attempt + 1} of {max_attempts}"
                    )
                    # Retry after 10 seconds
                    time.sleep(10)
                    attempt += 1
                    if attempt == max_attempts:
                        return None
