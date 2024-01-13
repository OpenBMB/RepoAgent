from jsonhandle import JsonFileProcessor
from vectordbs import ChromaManager
from prompt import TextAnalysisTool
from logger import LoggerManager
from llama_index import PromptTemplate 
from llama_index.llms import OpenAI



class RepoAssistant:
    def __init__(self, api_key, api_base, db_path, log_file):
        # Initialize OpenAI, database, and load JSON data
        logger=LoggerManager(log_file)
        self.logger=logger.get_logger()
        self.api_key = api_key
        self.api_base = api_base
        self.db_path = db_path
        self.md_contents=[]
        self.llm = OpenAI(api_key=api_key, api_base=api_base)
        textanslys=TextAnalysisTool(self.llm,logger,db_path)
        json_data = JsonFileProcessor(db_path)
        chroma_data=ChromaManager(api_key, api_base)
        self.textanslys=textanslys
        self.json_data = json_data
        self.chroma_data = chroma_data

    
    def generate_queries(self, query_str: str, num_queries: int = 4):
        query_gen_prompt_str = (
            "You are a helpful assistant that generates multiple search queries based on a "
            "single input query. Generate {num_queries} search queries, one on each line, "
            "related to the following input query:\n"
            "Query: {query}\n"
            "Queries:\n"
        )
        query_gen_prompt = PromptTemplate(query_gen_prompt_str)
        fmt_prompt = query_gen_prompt.format(
            num_queries=num_queries - 1, query=query_str
        )
        response = self.llm.complete(fmt_prompt)
        queries = response.text.split("\n")
        return queries
    
    def rag(self, query, retrieved_documents):
        # rag 
        information = "\n\n".join(retrieved_documents)
        messages = f"You are a helpful expert repo research assistant. Your users are asking questions about information contained in repo . You will be shown the user's question, and the relevant information from the repo. Answer the user's question using only this information.\nQuestion: {query}. \nInformation: {information}"
        response = self.llm.complete(messages)
        content = response
        return content
    
    def extract_and_format_documents(self, results):
        formatted_documents = ""
        for index, item in enumerate(results, start=1):
            # 从每个字典中提取 'documents' 键的值
            documents = item.get('documents', [[]])
            
            # 由于 'documents' 是一个列表的列表，我们需要提取第一个列表的元素
            for doc in documents[0]:
                formatted_documents += f"\n{index}: {doc}"
        return formatted_documents
    
    def respond(self, message, instruction):
        # return answer
        prompt = self.textanslys.format_chat_prompt(message, instruction)
        questions = self.textanslys.keyword(prompt)
        self.logger.debug(f"Questions: {questions}")
        promptq = self.generate_queries(prompt,3)
        result = []
        for i in promptq:
            result.append(self.chroma_data.chroma_collection.query(query_texts=[i], n_results=5))
        results=self.chroma_data.chroma_collection.query(query_texts=[prompt], n_results=5)
        self.logger.debug(f"Results: {results}")
        chunkrecall=self.extract_and_format_documents(result)
        retrieved_documents = results['documents'][0]
        response = self.rag(prompt,retrieved_documents)
        bot_message = str(response)
        keyword=str(self.textanslys.nerquery(bot_message))
        code='\n'+'```python'+'\n'+self.textanslys.queryblock(keyword)+'\n'+'```'
        bot_message=bot_message +'\n'+ str(self.textanslys.tree(bot_message))
        return "", bot_message,chunkrecall,questions,code,message
    
if __name__ == "__main__":
    api_key =""
    api_base =""
    db_path =""
    log_file =""
    assistant = RepoAssistant(api_key, api_base, db_path,log_file)