
import os
import gradio as gr
import chromadb
import openai
from llama_index import Document, VectorStoreIndex, ServiceContext, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.llms import OpenAI
from llama_index.node_parser import HierarchicalNodeParser, get_leaf_nodes
from llama_index.vector_stores import ChromaVectorStore
from llama_index.embeddings import OpenAIEmbedding
from llama_index.retrievers import AutoMergingRetriever
from llama_index.query_engine import RetrieverQueryEngine

# Class Definitions
class DocumentIndexer:
    def __init__(self, dir_path, required_exts):
        self.dir_path = dir_path
        self.required_exts = required_exts
        self.documents = []
        self.nodes = []
        self.leaf_nodes = []
        self.nodes_by_id = {}
        self.embed_model = OpenAIEmbedding()
        self.storage_context = StorageContext.from_defaults()
        self.service_context = ServiceContext.from_defaults(embed_model=self.embed_model)
        self.automerging_index = None

    def load_documents(self):
        # Load and parse documents
        documents = SimpleDirectoryReader(
            input_dir=self.dir_path,
            required_exts=self.required_exts,
            recursive=True,
        ).load_data()
        document = Document(text="\n\n".join([doc.text for doc in documents]))
        self.documents = documents
        return document

    def parse_documents(self, document):
        # Create node parser and get nodes
        node_parser = HierarchicalNodeParser.from_defaults(
            chunk_sizes=[2048, 512, 128]
        )
        self.nodes = node_parser.get_nodes_from_documents([document])
        self.leaf_nodes = get_leaf_nodes(self.nodes)
        self.nodes_by_id = {node.node_id: node for node in self.nodes}

    def create_index(self):
        # Create and persist index
        self.automerging_index = VectorStoreIndex(
            self.leaf_nodes, storage_context=self.storage_context, service_context=self.service_context
        )
        self.automerging_index.storage_context.persist(persist_dir="./merging_index")

class ChatbotResponder:
    def __init__(self, automerging_engine):
        self.automerging_engine = automerging_engine

    def respond(self, message, chat_history, instruction):
        prompt = message + instruction
        chat_history = chat_history + [[message, ""]]
        auto_merging_response = self.automerging_engine.query(prompt)
        bot_message = str(auto_merging_response)
        chat_history.append((message, bot_message))
        return "", chat_history

# Main Execution Block
if __name__ == "__main__":
    openai.api_key = 'sk-'
    openai.base_url = 'https://example.com'
    
    # Initialize DocumentIndexer and ChatbotResponder
    indexer = DocumentIndexer("../../Markdown_Docs/", [".md", ".py"])
    document = indexer.load_documents()
    indexer.parse_documents(document)
    indexer.create_index()
    automerging_index = indexer.automerging_index
    automerging_retriever = automerging_index.as_retriever(similarity_top_k=12)
    retriever = AutoMergingRetriever(
        automerging_retriever, 
        automerging_index.storage_context, 
        verbose=True
    )
    auto_merging_engine = RetrieverQueryEngine.from_args(automerging_retriever)
    responder = ChatbotResponder(auto_merging_engine)

    # Gradio Interface Setup
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(height=240)
        msg = gr.Textbox(label="Prompt")
        with gr.Accordion(label="Advanced options", open=False):
            system = gr.Textbox(label="System message", lines=2, value="A conversation between a user and an LLM-based AI assistant. The assistant gives helpful and honest answers.")
        
        btn = gr.Button("Submit")
        clear = gr.ClearButton(components=[msg, chatbot], value="Clear console")

        btn.click(responder.respond, inputs=[msg, chatbot, system], outputs=[msg, chatbot])
        msg.submit(responder.respond, inputs=[msg, chatbot, system], outputs=[msg, chatbot])

    gr.close_all()
    demo.queue().launch(share=True)
