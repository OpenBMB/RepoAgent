import os
import gradio as gr
import chromadb
import openai
from llama_index import Document,VectorStoreIndex,ServiceContext,SimpleDirectoryReader,StorageContext,load_index_from_storage
from llama_index.llms import OpenAI
from llama_index.node_parser import HierarchicalNodeParser,get_leaf_nodes
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import OpenAIEmbedding
from llama_index.retrievers import AutoMergingRetriever
from llama_index.query_engine import RetrieverQueryEngine
from chromadb.utils import embedding_functions
import json

class RepoAssistant:
    def __init__(self, api_key, api_base, db_path):
        # Initialize OpenAI, database, and load JSON data
        # ...
        self.api_key = api_key
        self.api_base = api_base
        self.db_path = db_path
        self.init_chroma_collection()
        self.llm=OpenAI(api_key = api_key,api_base = api_base,)


    def read_json_file(self, file_path):
        # ...
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data

    def extract_md_contents(self, json_data):
        # ...
        md_contents = []
        for file in json_data["files"]:
            for obj in file["objects"]:
                if "md_content" in obj:
                    md_contents.append(obj["md_content"])
        return md_contents
    
    def init_chroma_collection(self):
        chroma_client = chromadb.Client()
        self.chroma_collection = chroma_client.create_collection(
            "test", 
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_key=self.api_key,
                api_base=self.api_base,
                model_name="text-embedding-ada-002"
            )
        )

    def search_in_json_nested(self, file_path, search_text):
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
        # query = "Extract the most relevant class from the input text.input: " + message + "output:"
        query = "Extract the most relevant class or function from the following input:\n" + message + "\nOutput:"
        response = self.llm.complete(query)
        return response
    
    def queryblock(self,message):
        search_result = self.search_in_json_nested(self.db_path, message)
        # father=""
        if isinstance(search_result, dict):
        #     father=search_result['parent']
            search_result = search_result['code_content']
        return str(search_result)

    def create_vector_store(self, md_contents):
        ids = [str(i) for i in range(len(md_contents))]
        self.chroma_collection.add(ids=ids, documents=md_contents)


    def rag(self, query, retrieved_documents):
        # ...
        information = "\n\n".join(retrieved_documents)
        messages = f"You are a helpful expert repo research assistant. Your users are asking questions about information contained in repo . You will be shown the user's question, and the relevant information from the repo. Answer the user's question using only this information.\nQuestion: {query}. \nInformation: {information}"
        response = self.llm.complete(messages)
        content = response
        return content

    def Tree(self, query):
        # ...
        input_text = query
        prompt = f"Please analyze the following text and generate a tree structure based on its hierarchy:\n\n{input_text}"
        response = self.llm.complete(prompt)
        return response

    def format_chat_prompt(self, message, chat_history, instruction):
        # ...
        prompt = f"System:{instruction}"
        for turn in chat_history:
            user_message, bot_message = turn
            prompt = f"{prompt}\nUser: {user_message}\nAssistant: {bot_message}"
        prompt = f"{prompt}\nUser: {message}\nAssistant:"
        return prompt

    def respond(self, message, chat_history, instruction):
        # ...
        prompt = self.format_chat_prompt(message, chat_history, instruction)
        chat_history = chat_history + [[message, ""]]
        results = self.chroma_collection.query(query_texts=[prompt], n_results=5)
        retrieved_documents = results['documents'][0]
        response = self.rag(prompt,retrieved_documents)
        bot_message = str(response)
        keyword=str(self.NerQuery(bot_message))
        bot_message=bot_message +'\n'+ str(self.Tree(bot_message))+'\n'+'```python'+'\n'+self.queryblock(keyword)+'\n'+'```'
        # bot_message=bot_message +'\n'+ str(self.Tree(bot_message))
        chat_history.append((message, bot_message))
        return "", chat_history

    def setup_gradio_interface(self):
        # Gradio UI setupwith gr.Blocks() as demo:
        with gr.Blocks() as demo:
            chatbot = gr.Chatbot(height=540) #just to fit the notebook
            msg = gr.Textbox(label="Prompt")
            with gr.Accordion(label="Advanced options",open=False):
                system = gr.Textbox(label="System message", lines=2, value="A conversation between a user and an LLM-based AI assistant. The assistant gives helpful and honest answers.")
            btn = gr.Button("Submit")
            clear = gr.ClearButton(components=[msg, chatbot], value="Clear console")

            btn.click(self.respond, inputs=[msg, chatbot, system], outputs=[msg, chatbot])
            msg.submit(self.respond, inputs=[msg, chatbot, system], outputs=[msg, chatbot]) #Press enter to submit

        gr.close_all()
        demo.queue().launch(share=True)    

def main():
    api_key=''
    api_base='' 
    db_path = "./project_hierachy.json"

    assistant = RepoAssistant(api_key, api_base, db_path)
    json_data = assistant.read_json_file(db_path)
    md_contents = assistant.extract_md_contents(json_data)
    assistant.create_vector_store(md_contents)
    assistant.setup_gradio_interface()

if __name__ == "__main__":
    main()
