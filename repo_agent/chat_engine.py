import os,json
import re,sys
from openai import BadRequestError, OpenAI
from openai import APIConnectionError
import tiktoken
import time
from config import language_mapping
from project_manager import ProjectManager
from prompt import SYS_PROMPT, USR_PROMPT
import inspect


def get_import_statements():
    source_lines = inspect.getsourcelines(sys.modules[__name__])[0]
    import_lines = [line for line in source_lines if line.strip().startswith('import') or line.strip().startswith('from')]
    return import_lines


class ChatEngine:
    """
    ChatEngine is used to generate the doc of functions or classes.
    """
    def __init__(self, CONFIG):
        self.config = CONFIG

    def num_tokens_from_string(self, string: str, encoding_name = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def generate_doc(self, code_info, file_handler, referencer = []):

        #print("len(referencer):\n",len(referencer))

        def get_code_from_json(json_file, referencer):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            code_from_referencer = {}
            for ref in referencer:
                file_path, line_number, _ = ref
                if file_path in data:
                    objects = data[file_path]
                    min_obj = None
                    for obj_name, obj in objects.items():
                        if obj['code_start_line'] <= line_number <= obj['code_end_line']:
                            if min_obj is None or (obj['code_end_line'] - obj['code_start_line'] < min_obj['code_end_line'] - min_obj['code_start_line']):
                                min_obj = obj
                    if min_obj is not None:
                        if file_path not in code_from_referencer:
                            code_from_referencer[file_path] = []
                        code_from_referencer[file_path].append(min_obj['code_content'])
            return code_from_referencer
                
        code_type = code_info["type"]
        code_name = code_info["name"]
        code_content = code_info["code_content"]
        have_return = code_info["have_return"]

        project_manager = ProjectManager(repo_path=file_handler.repo_path, project_hierarchy=file_handler.project_hierarchy)
        project_structure = project_manager.get_project_structure()
        file_path = os.path.join(file_handler.repo_path, file_handler.file_path)
        code_from_referencer = get_code_from_json(project_manager.project_hierarchy, referencer) # 
        referenced = True if len(code_from_referencer) > 0 else False
        referencer_content = '\n'.join([f'File_Path:{file_path}\n' + '\n'.join([f'Corresponding code as follows:\n{code}\n[End of this part of code]' for code in codes]) + f'\n[End of {file_path}]' for file_path, codes in code_from_referencer.items()])

        # language
        language = self.config["language"]
        if language not in language_mapping:
            raise KeyError(f"Language code {language} is not given! Supported languages are: {json.dumps(language_mapping)}")
        
        language = language_mapping[language]
        
        code_type_tell = "Class" if code_type == "ClassDef" else "Function"
        have_return_tell = "**Output Example**: (Mock up a possible appearance of the code's return value.)" if have_return else ""
        reference_letter = "This object is called in the following files, the file paths and corresponding calling parts of the code are as follows:" if referenced else ""
        combine_ref_situation = "and combine it with its calling situation in the project," if referenced else ""
        
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
            referencer_content=referencer_content,
            language=language
            )
        
        usr_prompt = USR_PROMPT.format(language=language)
        
        # print("\nsys_prompt:\n",sys_prompt)
        # print("\nusr_prompt:\n",str(usr_prompt))

        max_attempts = 5  # 设置最大尝试次数
        model = self.config["default_completion_kwargs"]["model"]
        
        # 检查tokens长度
        if self.num_tokens_from_string(sys_prompt) + self.num_tokens_from_string(usr_prompt) >= 7100:
            print("The code is too long, using gpt-3.5-turbo-16k to process it.")
            model = "gpt-3.5-turbo-16k"
        
        attempt = 0
        while attempt < max_attempts:
            try:
                # 获取基本配置
                client = OpenAI(
                    api_key=self.config["api_keys"][model][0]["api_key"],
                    base_url=self.config["api_keys"][model][0]["base_url"],
                    timeout=self.config["default_completion_kwargs"]["request_timeout"]
                )

                messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": usr_prompt}]

                # print(f"message:\n{messages}\n")

                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=self.config["default_completion_kwargs"]["temperature"],
                    max_tokens=1024
                )

                response_message = response.choices[0].message

                # 如果 response_message 是 None，则继续下一次循环
                if response_message is None:
                    attempt += 1
                    continue

                print(f"\nAnswer:\n{response_message.content}\n")

                return response_message
            
            except APIConnectionError as e:
                print(f"Connection error: {e}. Attempt {attempt + 1} of {max_attempts}")
                # Retry after 7 seconds
                time.sleep(7)
                attempt += 1
                if attempt == max_attempts:
                    raise
                else:
                    continue # Try to request again

            except BadRequestError as e:
                if 'context_length_exceeded' in str(e):
                    print(f"Error: The model's maximum context length is exceeded. Reducing the length of the messages. Attempt {attempt + 1} of {max_attempts}")
                    # Set referenced to False and remove referencer_content
                    referenced = False
                    referencer_content = ""
                    reference_letter = ""
                    combine_ref_situation = ""
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
                        referencer_content=referencer_content,
                        language=language
                    )
                    attempt += 1
                    continue  # Try to request again
                else:
                    print(f"An OpenAI error occurred: {e}. Attempt {attempt + 1} of {max_attempts}")

            except Exception as e:
                print(f"An unknown error occurred: {e}. Attempt {attempt + 1} of {max_attempts}")
                # Retry after 10 seconds
                time.sleep(10)
                attempt += 1
                if attempt == max_attempts:
                    raise


