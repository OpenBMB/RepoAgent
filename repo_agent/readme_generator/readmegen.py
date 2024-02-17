import yaml
from genterated import OpenChatSummary
from dataacq import DataAquire
from llama_index.llms import OpenAI 
from loguru import logger

logger.add("./log.txt", level="DEBUG", format="{time} - {name} - {level} - {message}")


def read_yaml(file_path):
    """
    Read a YAML file and return the data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_readme(yaml_data, output_file):
    """
    Create a README file from YAML data.
    """
    readme_content = ""

    # 遍历YAML数据，将每个键值对转换为Markdown格式
    for key, value in yaml_data.items():
        appendix_content = read_yaml("./userappend.yml")["appendix"]
        appendix_content = "This is additional information "+appendix_content
        if key.lower() == 'name':
            info = str(data.summaryinfo())+appendix_content
            valuea=clients.processname(info,str(data.tree()),value)
            logger.debug(f"名字: {info}")
            # logger.debug(f"循环完: {str(data.tree())}")
            readme_content += f"{valuea}\n\n"
            # logger.debug(f"循环完: {readme_content}")
        if key.lower() == 'description':
            info = str(data.summaryinfo()) + appendix_content
            logger.debug(f"描述: {info}")
            valuea=clients.processdes(info,str(data.tree()),value)
            readme_content += f">{valuea}\n\n"
        if key.lower() == 'license':
            info = str(data.extract_license()) + appendix_content
            valuea=clients.processlinces(info,value)
            logger.debug(f"许可: {valuea}")
            readme_content += f"{valuea}\n\n"
        if key.lower() == 'installation':
            info = str(data.extract_requirements()) + appendix_content
            valuea=clients.processother(info,str(data.tree()),value)
            readme_content += f"{valuea}\n\n"
        if key.lower() == 'usage':
            info = str(data.extract_config_guide()) + str(data.summaryinfo()) + appendix_content
            valuea=clients.processother(info,str(data.tree()),value)
            readme_content += f"{valuea}\n\n"
        appendix_functions = ['badges', 'visuals','support', 'roadmap', 'authors_and_acknowledgment', 'project_status', 'citation']
        for section in appendix_functions:
            if section in appendix_content:
                valuea=clients.processother(appendix_content,str(data.tree()),value)
                readme_content += f"{valuea}\n\n"
                # 调用对应的函数
    # 将生成的内容写入到README文件中
    logger.debug(f"重构前: {readme_content}")
    readme_content = clients.refactor(readme_content)
    logger.debug(f"重构完: {readme_content}")
    readme_content = str(readme_content)
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(readme_content)

    print(f"{output_file} file created successfully.")


if __name__ == "__main__":
    config = read_yaml("config.yml")
    api_key = config['api_key']
    api_base = config['api_base']
    path = config['repo']
    clients = OpenChatSummary(api_key, api_base)
    data = DataAquire(path)
    # 读取YAML文件
    yaml_data = read_yaml("./template.yml")

    # 创建README文件
    create_readme(yaml_data, "README.md")
