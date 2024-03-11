import inspect
import os
import sys
import time
from dataclasses import dataclass

import tiktoken
from openai import APIConnectionError, OpenAI

from repo_agent.doc_meta_info import DocItem
from repo_agent.log import logger
from repo_agent.prompt import SYS_PROMPT, USR_PROMPT
from repo_agent.settings import max_input_tokens_map, setting


def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [
        line
        for line in source_lines
        if line.strip().startswith("import") or line.strip().startswith("from")
    ]
    return import_lines

@dataclass
class ResponseMessage:
    content: str


class ChatEngine:
    """
    ChatEngine is used to generate the doc of functions or classes.
    """

    def __init__(self, project_manager):
        self.project_manager = project_manager

    def num_tokens_from_string(self, string: str, encoding_name="cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def reduce_input_length(self, shorten_attempt, prompt_data):
        """
        Reduces the length of the input prompts by modifying the sys_prompt contents.
        """

        logger.info(
            f"Attempt {shorten_attempt + 1} / 2 to reduce the length of the messages."
        )
        if shorten_attempt == 0:
            # First attempt, remove project_structure and project_structure_prefix
            prompt_data.project_structure = ""
            prompt_data.project_structure_prefix = ""
        elif shorten_attempt == 1:
            # Second attempt, futher remove caller and callee (reference) information
            prompt_data.project_structure = ""
            prompt_data.project_structure_prefix = ""

            prompt_data.referenced = False
            prompt_data.referencer_content = ""
            prompt_data.reference_letter = ""
            prompt_data.combine_ref_situation = ""

        # Update sys_prompt
        sys_prompt = SYS_PROMPT.format(**prompt_data)

        return sys_prompt

    def generate_response(self, model, sys_prompt, usr_prompt, max_tokens):
        client = OpenAI(
            api_key=setting.chat_completion.openai_api_key.get_secret_value(),
            base_url=str(setting.chat_completion.base_url),
            timeout=setting.chat_completion.request_timeout,
        )

        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": usr_prompt},
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=setting.chat_completion.temperature,
            max_tokens=max_tokens,
        )

        response_message = response.choices[0].message

        return response_message

    def attempt_generate_response(
        self, model, sys_prompt, usr_prompt, max_tokens, max_attempts=5
    ):
        attempt = 0
        while attempt < max_attempts:
            try:
                response_message = self.generate_response(
                    model, sys_prompt, usr_prompt, max_tokens
                )

                # 如果 response_message 是 None，则继续下一次循环
                if response_message is None:
                    attempt += 1
                    continue
                return response_message

            except APIConnectionError as e:
                logger.error(
                    f"Connection error: {e}. Attempt {attempt + 1} of {max_attempts}"
                )
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
                    response_message = ResponseMessage(
                        "An unknown error occurred while generating this documentation after many tries."
                    )
                    return response_message

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
        doc_item_path = os.path.join(file_path, code_name)

        # 树结构路径通过全局信息中的who reference me 和 reference who + 自身的file_path来获取
        # 使用 ProjectManager 实例来获取项目结构
        project_structure = self.project_manager.build_path_tree(
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
                return "And please include the reference relationship with its callers and callees in the project from a functional perspective"
            elif referencer_content:
                return "And please include the relationship with its callers in the project from a functional perspective."
            elif reference_letter:
                return "And please include the relationship with its callees in the project from a functional perspective."
            else:
                return ""

        max_tokens = setting.project.max_document_tokens

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
        has_relationship = get_relationship_description(
            referencer_content, reference_letter
        )

        project_structure_prefix = ", and the related hierarchical structure of this project is as follows (The current object is marked with an *):"

        # 第一次尝试构建完整的prompt
        prompt_data = {
            "combine_ref_situation": combine_ref_situation,
            "file_path": file_path,
            "project_structure_prefix": project_structure_prefix,
            "project_structure": project_structure,
            "code_type_tell": code_type_tell,
            "code_name": code_name,
            "code_content": code_content,
            "have_return_tell": have_return_tell,
            "has_relationship": has_relationship,
            "reference_letter": reference_letter,
            "referencer_content": referencer_content,
            "parameters_or_attribute": parameters_or_attribute,
            "language": setting.project.language,
        }

        sys_prompt = SYS_PROMPT.format(**prompt_data)

        usr_prompt = USR_PROMPT.format(language=setting.project.language)

        model = setting.chat_completion.model
        max_input_length = max_input_tokens_map.get(model, 4096) - max_tokens

        total_tokens = self.num_tokens_from_string(
            sys_prompt
        ) + self.num_tokens_from_string(usr_prompt)

        # 如果总tokens超过当前模型的限制，则尝试寻找较大模型或者缩减输入
        if total_tokens >= max_input_length:
            # 查找一个拥有更大输入限制的模型
            larger_models = {
                k: v
                for k, v in max_input_tokens_map.items()
                if (v - max_tokens) > total_tokens
            }  # 抽取出所有上下文长度大于当前总输入tokens的模型
            for model_name, max_input_length in larger_models.items():
                if max_input_length - max_tokens > total_tokens:
                    try:
                        # Attempt to make a request with the larger model
                        logger.info(
                            f"Trying model {model_name} for large-context processing."
                        )
                        response_message = self.attempt_generate_response(
                            model_name, sys_prompt, usr_prompt, max_tokens
                        )  # response_message在attempt_generate_response中已经被校验过了
                        return response_message
                    except Exception as e:
                        # 否则直接跳过，尝试下一个模型
                        continue  # Try the next model
            # If no larger models succeed, fallback to original model
            # 对于最初的model模型，尝试缩减输入长度
            for shorten_attempt in range(2):
                shorten_success = False
                sys_prompt = self.reduce_input_length(shorten_attempt, prompt_data)
                # 重新计算 tokens
                total_tokens = self.num_tokens_from_string(
                    sys_prompt
                ) + self.num_tokens_from_string(usr_prompt)
                # 检查是否满足要求
                if total_tokens < max_input_length:
                    shorten_success = True
                    # 如满足要求直接发送请求来生成文档
                    response_message = self.attempt_generate_response(
                        model, sys_prompt, usr_prompt, max_tokens
                    )

            if not shorten_success:
                # 意味着这个doc_item无法生成doc（因为代码本身的长度就超过了模型的限制）
                # 返回一个自定义的response_message对象，它的content是"Tried to generate the document, but the code is too long to process."
                # 在其他代码调用的时候使用的是response_message.content，所以必须确保content能通过这种方式从response_message中被读取出来
                response_message = ResponseMessage(
                    "Tried to generate the document, but the code is too long to process."
                )
                return response_message

        else:  # 如果总tokens没有超过模型限制，直接发送请求
            response_message = self.attempt_generate_response(
                model, sys_prompt, usr_prompt, max_tokens
            )

        return response_message
