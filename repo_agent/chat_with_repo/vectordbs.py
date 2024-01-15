import chromadb
from chromadb.utils import embedding_functions


class ChromaManager:
    def __init__(self, api_key, api_base):
        self.api_key = api_key
        self.api_base = api_base
        self.chroma_collection = None
        self.init_chroma_collection()

    def init_chroma_collection(self):
        # Initialize Chroma VectorDB
        chroma_client = chromadb.Client()
        self.chroma_collection = chroma_client.create_collection(
            "test",
            embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key = self.api_key,
                api_base = self.api_base,
                model_name="text-embedding-ada-002"
            )
        )
        self.chroma_collection = chroma_client.get_collection(
            "test",
            embedding_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key = self.api_key,
                api_base = self.api_base,
                model_name = "text-embedding-ada-002"
            )
        )

    def create_vector_store(self, md_contents):
        # Process Markdown content and store it in Chroma
        self.md_contents = md_contents
        ids = [str(i) for i in range(len(md_contents))]
        embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key = self.api_key,
            api_base = self.api_base,
            model_name = "text-embedding-ada-002"
        )
        embeddings = embedding_function(md_contents)
        self.chroma_collection.add(ids = ids, documents = md_contents, embeddings = embeddings)

if __name__ == "__main__":
    test = ChromaManager(api_key = "", api_base = "")
    