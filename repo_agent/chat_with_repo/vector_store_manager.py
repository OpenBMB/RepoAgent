import chromadb
from llama_index.core import (
    Document,
    StorageContext,
    VectorStoreIndex,
    get_response_synthesizer,
)
from llama_index.core.node_parser import (
    SemanticSplitterNodeParser,
    SentenceSplitter,
)
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from repo_agent.log import logger


class VectorStoreManager:
    def __init__(self, top_k, llm):
        """
        Initialize the VectorStoreManager.
        """
        self.query_engine = None  # Initialize as None
        self.chroma_db_path = "./chroma_db"  # Path to Chroma database
        self.collection_name = "test"  # Default collection name
        self.similarity_top_k = top_k
        self.llm = llm

    def create_vector_store(self, md_contents, meta_data, api_key, api_base):
        """
        Add markdown content and metadata to the index.
        """
        if not md_contents or not meta_data:
            logger.warning("No content or metadata provided. Skipping.")
            return

        # Ensure lengths match
        min_length = min(len(md_contents), len(meta_data))
        md_contents = md_contents[:min_length]
        meta_data = meta_data[:min_length]

        logger.debug(f"Number of markdown contents: {len(md_contents)}")
        logger.debug(f"Number of metadata entries: {len(meta_data)}")

        # Initialize Chroma client and collection
        db = chromadb.PersistentClient(path=self.chroma_db_path)
        chroma_collection = db.get_or_create_collection(self.collection_name)

        # Define embedding model
        embed_model = OpenAIEmbedding(
            model_name="text-embedding-3-large",
            api_key=api_key,
            api_base=api_base,
        )

        # Initialize semantic chunker (SimpleNodeParser)
        logger.debug("Initializing semantic chunker (SimpleNodeParser).")
        splitter = SemanticSplitterNodeParser(
            buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
        )
        base_splitter = SentenceSplitter(chunk_size=1024)

        documents = [
            Document(text=content, extra_info=meta)
            for content, meta in zip(md_contents, meta_data)
        ]

        all_nodes = []
        for i, doc in enumerate(documents):
            logger.debug(
                f"Processing document {i+1}: Content length={len(doc.get_text())}"
            )

            try:
                # Try semantic splitting first
                nodes = splitter.get_nodes_from_documents([doc])
                logger.debug(f"Document {i+1} split into {len(nodes)} semantic chunks.")

            except Exception as e:
                # Fallback to baseline sentence splitting
                logger.warning(
                    f"Semantic splitting failed for document {i+1}, falling back to SentenceSplitter. Error: {e}"
                )
                nodes = base_splitter.get_nodes_from_documents([doc])
                logger.debug(f"Document {i+1} split into {len(nodes)} sentence chunks.")

            all_nodes.extend(nodes)

        if not all_nodes:
            logger.warning("No valid nodes to add to the index after chunking.")
            return

        logger.debug(f"Number of valid chunks: {len(all_nodes)}")

        # Set up ChromaVectorStore and load data
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex(
            all_nodes, storage_context=storage_context, embed_model=embed_model
        )
        retriever = VectorIndexRetriever(
            index=index, similarity_top_k=self.similarity_top_k, embed_model=embed_model
        )

        response_synthesizer = get_response_synthesizer(llm=self.llm)

        # Set the query engine
        self.query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
        )

        logger.info(f"Vector store created and loaded with {len(documents)} documents.")

    def query_store(self, query):
        """
        Query the vector store for relevant documents.
        """
        if not self.query_engine:
            logger.error(
                "Query engine is not initialized. Please create a vector store first."
            )
            return []

        # Query the vector store
        logger.debug(f"Querying vector store with: {query}")
        results = self.query_engine.query(query)

        # Extract relevant information from results
        return [{"text": results.response, "metadata": results.metadata}]
