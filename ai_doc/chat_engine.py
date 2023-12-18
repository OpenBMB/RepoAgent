import os,json
import re,sys
from openai import OpenAI
from openai import APIConnectionError
import yaml
import tiktoken
import time
from project_manager import ProjectManager
from Prompts.Sys_prompts.English.obj_doc_with_reference import SYS_PROMPT
from Prompts.Usr_prompts.English.usr_prompt import USR_PROMPT
import inspect


def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [line for line in source_lines if line.strip().startswith('import') or line.strip().startswith('from')]
    return import_lines


class ChatEngine:
    """
    文档生成器，用于生成函数或类的文档
    """
    def __init__(self, CONFIG):
        self.config = CONFIG

    def num_tokens_from_string(self, string: str, encoding_name = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def generate_doc(self, code_info, file_handler, referencer = []):

        def get_code_from_json(json_file, referencer):
            with open(json_file, 'r') as f:
                data = json.load(f)

            code_from_referencer = {}
            for ref in referencer:
                file_path, line_number, _ = ref
                for file in data["files"]:
                    if file['file_path'] == file_path:
                        min_obj = None
                        for obj in file['objects']:
                            if obj['code_start_line'] <= line_number <= obj['code_end_line']:
                                if min_obj is None or (obj['code_end_line'] - obj['code_start_line'] < min_obj['code_end_line'] - min_obj['code_start_line']):
                                    min_obj = obj
                        if min_obj is not None:
                            if file_path not in code_from_referencer:
                                code_from_referencer[file_path] = []
                            code_from_referencer[file_path].append(min_obj['code_content'])
            return code_from_referencer
        
        # 从code_info中获取代码信息
        code_type = code_info["type"]
        code_name = code_info["name"]
        code_content = code_info["code_content"]
        have_return = code_info["have_return"]

        # 初始化一个项目管理器
        project_manager = ProjectManager(repo_path=file_handler.repo_path, project_hierachy=file_handler.project_hierachy)
        project_structure = project_manager.get_project_structure()
        file_path = os.path.join(file_handler.repo_path, file_handler.file_path)
        # TODO:由于Jedi并行调用会出错，all_referencer应该在外面统一生成，并根据对象作为参数传入
        code_from_referencer = get_code_from_json(project_manager.project_hierachy, referencer) # 
        referenced = True if len(code_from_referencer) > 0 else False
        referencer_content = '\n'.join([f'File_Path:{file_path}\n' + '\nCorresponding code as follows:\n'.join(codes) + "="*30 for file_path, codes in code_from_referencer.items()])     

        # 判断及占位符
        model = "gpt-4"

        # 判断导入文件的时候SYS.PROMPT来自English还是Chinese
        import_lines = get_import_statements()

        for line in import_lines:
            match = re.search(r'Prompts\.Usr_prompts\.(\w+)\.usr_prompt', line)
            if match:
                language = match.group(1)
        if language == "English":

            code_type_tell = "Class" if code_type == "ClassDef" else "Function"
            have_return_tell = "**Output Example**: Mock up a possible appearance of the code's return value." if have_return else ""
            reference_letter = "This object is called in the following files, the file paths and corresponding calling parts of the code are as follows:" if referenced else ""
            combine_ref_situation = "and combine it with its calling situation in the project," if referenced else ""
        else:
            code_type_tell = "类" if code_type == "ClassDef" else "函数"
            have_return_tell = "**输出示例**：请你Mock出代码返回值的可能样例..." if have_return else ""
            reference_letter = "该对象在以下文件中被调用，文件路径和对应的调用代码如下：" if referenced else ""
            combine_ref_situation = "结合它在项目中的调用情况，" if referenced else ""

        sys_prompt = SYS_PROMPT.format(
            reference_letter=reference_letter, 
            combine_ref_situation=combine_ref_situation, 
            file_path=file_path, 
            project_structure=project_structure, 
            code_type_tell=code_type_tell, 
            code_name=code_name, 
            code_content=code_content, 
            have_return_tell=have_return_tell, 
            referenced=referenced, 
            referencer_content=referencer_content
            )
        
        usr_prompt = USR_PROMPT

        max_attempts = 5  # 设置最大尝试次数

        for attempt in range(max_attempts):
            try:
                # 检查tokens长度
                if self.num_tokens_from_string(sys_prompt) + self.num_tokens_from_string(usr_prompt) < 3500:
                    model = "gpt-4"
                else:
                    print("The code is too long, using gpt-3.5-turbo-16k to process it.")
                    model = "gpt-3.5-turbo-16k"
                    
                # 获取基本配置
                client = OpenAI(
                    api_key=self.config["api_keys"][model][0]["api_key"],
                    base_url=self.config["api_keys"][model][0]["base_url"],
                )

                messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": usr_prompt}]

                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0,
                )

                response_message = response.choices[0].message
                print("response.choices[0]:\n",response.choices[0])

                return response_message
            
            except APIConnectionError as e:
                print(f"Connection error: {e}. Attempt {attempt + 1} of {max_attempts}")
                # 等待7秒后重试
                time.sleep(7)
                if attempt + 1 == max_attempts:
                    raise
            except Exception as e:
                print(f"An error occurred: {e}. Attempt {attempt + 1} of {max_attempts}")
                # 等待10秒后重试
                time.sleep(10)
                if attempt + 1 == max_attempts:
                    raise


