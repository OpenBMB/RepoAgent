import os
import gradio as gr
import chromadb
import openai
import json
import logging
from llama_index import Document,VectorStoreIndex,ServiceContext,SimpleDirectoryReader,StorageContext,load_index_from_storage
from llama_index.llms import OpenAI
from llama_index.node_parser import HierarchicalNodeParser,get_leaf_nodes
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import OpenAIEmbedding
from llama_index.retrievers import AutoMergingRetriever
from llama_index.query_engine import RetrieverQueryEngine
from chromadb.utils import embedding_functions


class RepoAssistant:
    def __init__(self, api_key, api_base, db_path, log_file):
        # Initialize OpenAI, database, and load JSON data
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG) 
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG) 
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.api_key = api_key
        self.api_base = api_base
        self.db_path = db_path
        self.init_chroma_collection()
        self.llm = OpenAI(api_key=api_key, api_base=api_base)

    def read_json_file(self, file_path):
        #  read json file as database
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def extract_md_contents(self, json_data):
        # find json file summary md_content return a list
        md_contents = []
        for file in json_data["files"]:
            for obj in file["objects"]:
                if "md_content" in obj:
                    md_contents.append(obj["md_content"])
        return md_contents
    
    def init_chroma_collection(self):
        # init chroma vectordb
        chroma_client = chromadb.Client()
        self.chroma_collection = chroma_client.create_collection(
            "test", 
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_key=self.api_key,
                api_base=self.api_base,
                model_name="text-embedding-ada-002"
            )
        )
        self.chroma_collection = chroma_client.get_collection(
            "test", 
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_key=self.api_key,
                api_base=self.api_base,
                model_name="text-embedding-ada-002"
            )
        )

    def search_in_json_nested(self, file_path, search_text):
        # retrieve code from json
        try:
            with open(file_path, 'r',encoding='utf-8') as file:
                data = json.load(file)

                def recursive_search(data_item):
                    if isinstance(data_item, dict):
                        if 'name' in data_item and search_text.lower() in data_item['name'].lower():
                            return data_item

                        for key, value in data_item.items():
                            if isinstance(value, (dict, list)):
                                result = recursive_search(value)
                                if result:
                                    return result
                    elif isinstance(data_item, list):
                        for item in data_item:
                            result = recursive_search(item)
                            if result:
                                return result

                result = recursive_search(data)
                if result:
                    return result
                else:
                    return "No matching item found."

        except FileNotFoundError:
            return "File not found."
        except json.JSONDecodeError:
            return "Invalid JSON file."
        except Exception as e:
            return f"An error occurred: {e}"

    def NerQuery(self,message):
        # summery main related function of class
        query1 = """
                The output must strictly be a pure function name or class name, without any additional characters.
                For example:
                Pure function names: calculateSum, processData
                Pure class names: MyClass, DataProcessor
                The output function name or class name should be only one.
                """
        query = "Extract the most relevant class or function from the following"+query1+"input:\n" + message + "\nOutput:"
        response = self.llm.complete(query)
        self.logger.debug(f"Input: {message}, Output: {response}")
        return response
    
    def queryblock(self,message):
        # return a code block for retrieval
        search_result = self.search_in_json_nested(self.db_path, message)
        if isinstance(search_result, dict):
            search_result = search_result['code_content']
        return str(search_result)

    def create_vector_store(self, md_contents):
        # deal with md_content put it into chroma and embedding it 
        ids = [str(i) for i in range(len(md_contents))]
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_key=self.api_key,
                api_base=self.api_base,
                model_name="text-embedding-ada-002"
            )
        embeddings=embedding_function(md_contents)
        self.chroma_collection.add(ids=ids, documents=md_contents,embeddings=embeddings)
        added_docs_count = len(ids)
        self.logger.info(f"Added {added_docs_count} documents to the chroma collection.")

        metadata = self.chroma_collection.get_metadata() if hasattr(self.chroma_collection, 'get_metadata') else "No metadata method available"
        self.logger.info(f"Chroma collection metadata: {metadata}")
        metadata2= self.chroma_collection.get_embeddings() if hasattr(self.chroma_collection, 'get_embeddings') else "No metadata method available"
        self.logger.info(f"Chroma collection embeddings: {metadata2}")


    def rag(self, query, retrieved_documents):
        # rag 
        information = "\n\n".join(retrieved_documents)
        messages = f"You are a helpful expert repo research assistant. Your users are asking questions about information contained in repo . You will be shown the user's question, and the relevant information from the repo. Answer the user's question using only this information.\nQuestion: {query}. \nInformation: {information}"
        response = self.llm.complete(messages)
        content = response
        return content

    def Tree(self, query):
        # show a tree structure
        input_text = query
        prompt = f"Please analyze the following text and generate a tree structure based on its hierarchy:\n\n{input_text}"
        response = self.llm.complete(prompt)
        return response

    def format_chat_prompt(self, message,instruction):
        #  format prompt
        prompt = f"System:{instruction}"
        prompt = f"{prompt}\nUser: {message}\nAssistant:"
        return prompt

    def respond(self, message, instruction):
        # return answer
        prompt = self.format_chat_prompt(message, instruction)
        results = self.chroma_collection.query(query_texts=[prompt], n_results=5)
        self.logger.debug(f"Results: {results}")
        retrieved_documents = results['documents'][0]
        response = self.rag(prompt,retrieved_documents)
        bot_message = str(response)
        keyword=str(self.NerQuery(bot_message))
        code='\n'+'```python'+'\n'+self.queryblock(keyword)+'\n'+'```'
        bot_message=bot_message +'\n'+ str(self.Tree(bot_message))+code
        return "", bot_message,results,keyword,code,message





    def setup_gradio_interface(self):
        # Gradio UI setup with gr.Blocks() as demo
        with gr.Blocks() as demo:
            gr.Markdown(
                """
                # RepoChat Test
                This is a test for retrieval repo 
                """)
            with gr.Row():
                with gr.Column():

                    msg = gr.Textbox(label="Prompt")
                    with gr.Accordion(label="Advanced options", open=False):
                        system = gr.Textbox(label="System message", lines=2, value="A conversation between a user and an LLM-based AI assistant. The assistant gives helpful and honest answers.")
                    gr.Markdown("### rag")
                    output1 = gr.Markdown(label="RAG")
                    btn = gr.Button("Submit")

                with gr.Column():
                    output2 = gr.Textbox(label="Embedding recall")
                with gr.Column():
                    gr.Markdown("### question")
                    question = gr.Markdown(label="qa")
                    output3 = gr.Textbox(label="key words")
                    gr.Markdown("### code")
                    code = gr.Markdown(label="code")

            btn.click(self.respond, inputs=[msg, system], outputs=[msg, output1,output2,output3,code,question])
            msg.submit(self.respond, inputs=[msg, system], outputs=[msg, output1,output2,output3,code,question])  # Press enter to submit

        gr.close_all()
        demo.queue().launch(share=True)

def main():
    api_key=""
    api_base=""
    db_path = "./project_hierachy.json"
    log_file= "./log.txt"
    assistant = RepoAssistant(api_key, api_base, db_path,log_file)
    json_data = assistant.read_json_file(db_path)
    md_contents = assistant.extract_md_contents(json_data)
    assistant.create_vector_store(md_contents)
    assistant.setup_gradio_interface()

if __name__ == "__main__":
    main()
