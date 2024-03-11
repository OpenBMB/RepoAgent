from llama_index.llms import OpenAI

from repo_agent.chat_with_repo.json_handler import JsonFileProcessor
from repo_agent.log import logger


class TextAnalysisTool:
    def __init__(self, llm, db_path):
        self.jsonsearch = JsonFileProcessor(db_path)
        self.llm = llm
        self.db_path = db_path

    def keyword(self, query):
        prompt = f"Please provide a list of Code keywords according to the following query, please output no more than 3 keywords, Input: {query}, Output:"
        response = self.llm.complete(prompt)
        return response

    def tree(self, query):
        prompt = f"Please analyze the following text and generate a tree structure based on its hierarchy:\n\n{query}"
        response = self.llm.complete(prompt)
        return response

    def format_chat_prompt(self, message, instruction):
        prompt = f"System:{instruction}\nUser: {message}\nAssistant:"
        return prompt

    def queryblock(self, message):
        search_result,md = self.jsonsearch.search_code_contents_by_name(self.db_path, message)
        return search_result,md
    
    def list_to_markdown(self, search_result):
        markdown_str = ""
        # 遍历列表，将每个元素转换为Markdown格式的项
        for index, content in enumerate(search_result, start=1):
            # 添加到Markdown字符串中，每个项后跟一个换行符
            markdown_str += f"{index}. {content}\n\n"
        
        return markdown_str

    def nerquery(self, message):
        instrcution = """
Extract the most relevant class or function base on the following instrcution:

The output must strictly be a pure function name or class name, without any additional characters.
For example:
Pure function names: calculateSum, processData
Pure class names: MyClass, DataProcessor
The output function name or class name should be only one.
        """
        query = f"{instrcution}\n\nThe input is shown as bellow:\n{message}\n\nAnd now directly give your Output:"
        response = self.llm.complete(query)
        # logger.debug(f"Input: {message}, Output: {response}")
        return response

if __name__ == "__main__":
    api_base = "https://api.openai.com/v1"
    api_key = "your_api_key"
    log_file = "your_logfile_path"
    llm = OpenAI(api_key=api_key, api_base=api_base)
    db_path = "your_database_path"
    test = TextAnalysisTool(llm, db_path)
