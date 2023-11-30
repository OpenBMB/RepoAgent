import os
import re
from openai import OpenAI
from openai import APIConnectionError
import yaml
import tiktoken
import time


class ChatEngine:
    """
    文档生成器，用于生成函数或类的文档
    """
    def __init__(self, config_file):
        self.config = self.get_default_config(config_file=config_file)

    @staticmethod
    def get_default_config(config_file):
        """
        函数的作用是读取配置文件，返回一个字典
        输出示例：{'api_keys': {'gpt-3.5-turbo-16k': [{'api_key': 'sk-XXXX', 'base_url': 'https://example.com', 'api_type': 'azure', 'api_version': 'XXX', 'engine': 'GPT-35-Turbo-16k'}, {'api_key': 'sk-xxxxx', 'organization': 'org-xxxxxx', 'model': 'gpt-3.5-turbo-16k'}], 'gpt-4': [{'api_key': 'sk-XXXX', 'base_url': '', 'model': 'gpt-4'}], 'gpt-4-32k': [{'api_key': 'sk-XXXX', 'base_url': '', 'api_type': 'XXX', 'api_version': 'XXX', 'engine': 'gpt4-32'}]}}
        """
        try:
            config_file = os.getenv('CONFIG_FILE', config_file)
            cfg = yaml.load(open(config_file, 'r'), Loader=yaml.FullLoader)
        except Exception as e:
            cfg = {}
            print("my_exception",e)
        return cfg
    

    def num_tokens_from_string(self, string: str, encoding_name = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def generate_doc(self, code_info):
        code_type = code_info["type"]
        code_name = code_info["name"]
        code_content = code_info["content"]
        have_return = code_info["have_return"]
        model = "gpt-4"
        code_type_tell = "类" if code_type == "ClassDef" else "函数"
        have_return_tell = "**输出示例**：XXX" if have_return else ""
        sys_prompt = f"""
你是一个AI文档助手，你的任务是根据给定的函数或类的代码，生成对应的Markdown文档。文档的作用是帮助开发者和初学用户理解代码的作用和具体用法。
现在这段代码是一个{code_type_tell},这个{code_type_tell}的名字是{code_name}。
请你首先用markdown语法的一级标题写出{code_type_tell}的名称,随后用加粗的普通文本写出这个{code_type_tell}的作用，最后用普通文本给出详细的解析（需要包含一切细节），来作为这部分代码的文档。

格式标准案例如下：

# {code_name}
**{code_type_tell}作用** ：这个{code_type_tell}的作用是XXX

（详细的代码解析和描述...）

{have_return_tell}

"""
        usr_prompt = f"""
代码内容如下：
    {code_content}
请注意，你的开头一定是# {code_name}，除此之外，你生成的其他部分不要再包含markdown分级标题语法的内容。
请直接给出代码文档的中文回答：
"""
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
                # print("response.choices[0]:\n",response.choices[0])

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



if __name__ == "__main__":
    config_file = '/Users/logic/Documents/VisualStudioWorkspace/AI_doc/config.yml'
    chat_engine = ChatEngine(config_file=config_file)
    code_type = "FunctionDef" # ClassDef or FunctionDef
    code_name = "to_code"
    code_content = """
    def to_code(self):
        if self.code != []:
            return self.code
        self.code = self.gen_code()
        return self.code
    """
    code_info = {"type": code_type, "name": code_name, "content": code_content, "have_return": True}
    response_message = chat_engine.generate_doc(code_info)
    # print("response_message:\n",response_message)
    print("\nDone.\n")
