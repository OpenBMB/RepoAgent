from json_handle import JsonFileProcessor
from vectordbs import ChromaManager
from prompt import TextAnalysisTool
from loguru import logger
from llama_index import PromptTemplate 
from llama_index.llms import OpenAI 

logger.add("./log.txt", level="DEBUG", format="{time} - {name} - {level} - {message}")

class RepoAssistant:
    def __init__(self, api_key, api_base, db_path):
        # Initialize OpenAI, database, and load JSON data
        self.api_key = api_key
        self.api_base = api_base
        self.db_path = db_path
        self.md_contents = []
        self.llm = OpenAI(api_key=api_key, api_base=api_base)
        self.client = OpenAI(api_key=api_key, api_base=api_base,model="gpt-4-32k")
        self.textanslys = TextAnalysisTool(self.llm,db_path)
        self.json_data = JsonFileProcessor(db_path)
        self.chroma_data = ChromaManager(api_key, api_base)

    
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
            num_queries = num_queries - 1, query=query_str
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
    def list_to_markdown(self,list_items):
        markdown_content = ""
        
        # 对于列表中的每个项目，添加一个带数字的列表项
        for index, item in enumerate(list_items, start=1):
            markdown_content += f"{index}. {item}\n"

        return markdown_content
    def rag_ar(self, query, related_code, embedding_recall, project_name):
            message_sys = f"""
                You are a helpful Repository-Level Software Q&A assistant. Your task is to answer users questions based on given information about a software repository, including related code and documents. 

                Currently, you're in the {project_name} project. The user's question is:
                {query}

                Now, you are given related code and documents as follows:

                -------------------Code-------------------
                Some most likely related code snippets recalled by the retriever are:
                {related_code}

                -------------------Document-------------------
                Some most relevant documents recalled by the retriever are:
                {embedding_recall}

                Please note:   
                1. All the provided recall results are related to the current project {project_name}. Please filter useful information according to the user's question and provide corresponding answers or solutions.
                2. Ensure that your responses are accurate and detailed. Present specific answers in a professional manner and tone. If you find the user's question completely unrelated to the provided information or if you believe you cannot provide an accurate answer, kindly decline. Note: DO NOT fabricate any non-existent information.

                Now, focusing on the user's query, and incorporating the given information to offer a specific, detailed, and professional answer IN THE SAME LANGUAGE AS the user's question.
            """
            response = self.client.complete(message_sys)
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
        # logger.debug(f"Questions: {questions}")
        promptq = self.generate_queries(prompt,3)
        all_results = []
        all_ids = []
        for i in promptq:
            query_result = self.chroma_data.chroma_collection.query(query_texts = [i], n_results = 5,include=['documents','metadatas'])
            all_results.append(query_result)
            all_ids.extend(query_result['ids'][0])
        
        unique_ids = [id for id in all_ids if all_ids.count(id) == 1]
        # logger.debug(f"uniqueid: {unique_ids}")
        unique_documents = []
        unique_code = []
        for result in all_results:
            for id, doc , code in zip(result['ids'][0], result['documents'][0],result['metadatas'][0]):
                if id in unique_ids:
                    unique_documents.append(doc)
                    unique_code.append(code.get("code_content"))
    
        retrieved_documents=unique_documents
        # logger.debug(f"retrieveddocuments: {retrieved_documents}")
        response = self.rag(prompt,retrieved_documents)
        chunkrecall = self.list_to_markdown(retrieved_documents)
        bot_message = str(response)
        keyword = str(self.textanslys.nerquery(bot_message))
        codex='\n'+'```python'+'\n'+self.textanslys.queryblock(keyword)+'\n'+'```'
        unique_code.append(codex)
        bot_message = self.rag_ar(prompt,unique_code,retrieved_documents,"test")
        bot_message = str(bot_message) +'\n'+ str(self.textanslys.tree(bot_message))
        return message, bot_message,chunkrecall,questions,unique_code
    
if __name__ == "__main__":
    api_key = ""
    api_base = ""
    db_path = ""
    log_file = ""
    assistant = RepoAssistant(api_key, api_base, db_path,log_file)