import os
import openai
from openai import OpenAI
from loguru import logger
import yaml

logger.add("./log.txt", level="DEBUG", format="{time} - {name} - {level} - {message}")


def read_yaml(file_path):
    """
    Read a YAML file and return the data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def generate_summary(text):

    prompt="Remember I noly need the descripions about program, the usage info, please Summarize the following text:\n\n" + text
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt}
    
        ]
        )

    return completion.choices[0].message.content

def process_content(original_content):
    # 这里可以添加您自己的内容处理逻辑
    # 现在仅仅是复制原内容
    prompt = """
    Extract key information from the provided functional description for use in writing a README file. Pay attention to the following points:

        1. **Name of class or library**: Identify the name of the class or library mentioned in the description.
        2. **Main functions**: Summarize the core functions of the class or library, that is, what it is used for.
        3. **Initialization method** (if mentioned): Extracts information about the instance of the initialized class, such as the constructor and its parameters.
        4. **Dependencies and Third-Party Libraries**: Pay attention to any dependencies or third-party libraries mentioned in the description, this is very important for setup and installation.
        5. **Main methods and operations**:
        - Determine the name of each major method or operation.
        - Extract the purpose, input parameters, and return value of each method.
        6. **Sample Usage** (if available): Look for any code examples or usage instructions that may be included in the description.
        7. **Installation and Configuration Requirements** (if mentioned): Pay attention to any instructions on how to install or configure a class or library.
        8. **Additional Resources** (if mentioned): Include links to additional documentation, community forums, or other relevant resources.

    The focus is on extracting the precision and usefulness of this information in order to integrate it into a structured and informative README document.
    Here is an output example:
    '
    ClassDef XXX:

    Function description: XXX
    Initialization function __init__: receives the code library path repo_path, creates and saves the git warehouse object as the repo attribute.
    Third-party libraries used: git, subprocess, re.
    Method get_staged_pys:

    Function: Get the staged Python file changes in the warehouse.
    Return: Returns a dictionary, the key is the file path, and the value is a Boolean value indicating whether the file is newly created.
    Method get_changed_pys:

    Function: Get the changed Python files in the warehouse, including unstaged changes and untracked files.
    Returns: Returns a dictionary with the same structure as get_staged_pys.
    Method get_file_diff:

    
    '
    if we can't extract any relevant info return 'there's no relevant info' and igore the brefore instruct
    below is provided functional description 

    """
    prompt_content = prompt+original_content
    completion = client.chat.completions.create(
        model="gpt-4-32k",
        messages=[
            {"role": "system", "content": prompt_content}
        ]
        )

    return completion.choices[0].message.content

def create_new_docs(source_directory, target_directory):
    # 确保目标目录存在
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # 遍历源目录下的所有文件
    for filename in os.listdir(source_directory):
        source_file = os.path.join(source_directory, filename)
        
        # 检查是否为文件
        if os.path.isfile(source_file):
            # 读取原文件内容
            with open(source_file, 'r', encoding = 'utf-8') as file:
                content = file.read()

            # 处理内容
            processed_content = str(process_content(content))

            # 创建新文件名并保存在目标目录
            new_filename = os.path.splitext(filename)[0] + "_new.md"
            target_file = os.path.join(target_directory, new_filename)

            # 写入处理后的内容到新文件
            with open(target_file, 'w', encoding = 'utf-8') as new_file:
                new_file.write(processed_content)

def process_folder(folder_path):
    files = os.listdir(folder_path)
    combined_summary = ""

    for file in files:
        file_path = os.path.join(folder_path, file)
        
        with open(file_path, 'r' , encoding = 'utf-8') as f:
            content = f.read()
        logger.debug(f"Questions: {content}")
        current_summary = str(generate_summary(content))
        logger.debug(f"Questions: {current_summary}")
        combined_summary = str(generate_summary(combined_summary + " " + current_summary))
    with open(os.path.join(folder_path, "summary.md"), 'w', encoding = 'utf-8') as f:
        f.write(combined_summary)


if __name__ == "__main__":
    config = read_yaml("config.yml")
    api_key = config['api_key']
    api_base = config['api_base']
    client = OpenAI(api_key=api_key, base_url=api_base)
    # 调用函数，处理指定文件夹
    folder_path = config['markdownrepo']
    target_directory = './compressmd'
    os.makedirs(target_directory, exist_ok=True)

    create_new_docs(folder_path, target_directory)
    process_folder(target_directory)
