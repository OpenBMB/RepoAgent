import json

from llama_index import PromptTemplate
from llama_index.llms import OpenAI
from openai import OpenAI as AI

from repo_agent.chat_with_repo.json_handler import JsonFileProcessor
from repo_agent.chat_with_repo.prompt import TextAnalysisTool
from repo_agent.chat_with_repo.vectordb import ChromaManager
from repo_agent.log import logger


class RepoAssistant:
    def __init__(self, api_key, api_base, db_path):
        # Initialize OpenAI, database, and load JSON data
        self.api_key = api_key
        self.api_base = api_base
        self.db_path = db_path
        self.md_contents = []
        self.llm = OpenAI(api_key=api_key, api_base=api_base,model="gpt-3.5-turbo-1106")
        self.client = OpenAI(api_key=api_key, api_base=api_base,model="gpt-4-1106-preview")
        self.lm = AI(api_key = api_key, base_url = api_base)
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
    
    def rerank(self, query ,docs): # 这里要防止返回值格式上出问题
        response = self.lm.chat.completions.create(
            model='gpt-4-1106-preview',
            response_format={"type": "json_object"},
            temperature=0,
            messages=[
            {"role": "system", "content": "You are an expert relevance ranker. Given a list of documents and a query, your job is to determine how relevant each document is for answering the query. Your output is JSON, which is a list of documents.  Each document has two fields, content and score.  relevance_score is from 0.0 to 100.0. Higher relevance means higher score."},
            {"role": "user", "content": f"Query: {query} Docs: {docs}"}
            ]
        )
        scores = json.loads(response.choices[0].message.content)["documents"]
        logger.debug(f"scores: {scores}")
        sorted_data = sorted(scores, key=lambda x: x['relevance_score'], reverse=True)
        top_5_contents = [doc['content'] for doc in sorted_data[:5]]
        return top_5_contents

    def rag(self, query, retrieved_documents):
        # rag 
        information = "\n\n".join(retrieved_documents)
        messages = f"You are a helpful assistant in repository Q&A . Users will ask questions about something contained in a repository . You will be shown the user's question, and the relevant information from the repository. Answer the user's question only with information given.\n\nQuestion: {query}. \n\nInformation: {information}"
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
        
        logger.debug(f"all_ids: {all_ids},{all_results}")
        unique_ids = list(dict.fromkeys(all_ids))
        # unique_ids = [id for id in all_ids if all_ids.count(id) == 1]
        logger.debug(f"uniqueid: {unique_ids}")
        unique_documents = []
        unique_code = []
        for result in all_results:
            for id, doc , code in zip(result['ids'][0], result['documents'][0],result['metadatas'][0]):
                if id in unique_ids:
                    unique_documents.append(doc)
                    unique_code.append(code.get("code_content"))
        
        retrieved_documents = self.rerank(message,unique_documents)
        # logger.debug(f"retrieveddocuments: {retrieved_documents}")
        response = self.rag(prompt,retrieved_documents)
        chunkrecall = self.list_to_markdown(retrieved_documents)
        bot_message = str(response)
        keyword = str(self.textanslys.nerquery(bot_message))
        keywords = str(self.textanslys.nerquery(str(prompt)+str(questions)))
        codez,mdz=self.textanslys.queryblock(keyword)
        codey,mdy=self.textanslys.queryblock(keywords)
        if not isinstance(codez, list):
            codez = [codez]
        if not isinstance(mdz, list):
            mdz = [mdz]
        # 确保 codey 是列表，如果不是，则将其转换为列表
        if not isinstance(codey, list):
            codey = [codey]
        if not isinstance(mdy, list):
            mdy = [mdy]
        
        codex = codez+codey
        md = mdz + mdy
        unique_mdx = list(set([item for sublist in md for item in sublist]))
        uni_codex = []
        uni_md = []
        uni_codex = list(dict.fromkeys(codex))
        uni_md = list(dict.fromkeys(unique_mdx))
        codex = self.textanslys.list_to_markdown(uni_codex)
        retrieved_documents = retrieved_documents+uni_md
        retrieved_documents = list(dict.fromkeys(retrieved_documents))
        retrieved_documents = self.rerank(message,retrieved_documents[:6])
        uni_code = uni_codex+unique_code
        uni_code = list(dict.fromkeys(uni_code))
        uni_code = self.rerank(message,uni_code[:6])
        unique_code=self.textanslys.list_to_markdown(unique_code)
        bot_message = self.rag_ar(prompt,uni_code,retrieved_documents,"test")
        bot_message = str(bot_message)
        return message, bot_message, chunkrecall, questions, unique_code, codex


if __name__ == "__main__":
    api_key = ""
    api_base = ""
    db_path = ""
    log_file = ""
    assistant = RepoAssistant(api_key, api_base, db_path, log_file)
