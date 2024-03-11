import chromadb
from chromadb.utils import embedding_functions

from repo_agent.log import logger


class ChromaManager:
    def __init__(self, api_key, api_base):
        self.api_key = api_key
        self.api_base = api_base
        self.chroma_collection = None
        self.is_new_collection = False 
        self.init_chroma_collection()

    def init_chroma_collection(self):

        chroma_client = chromadb.PersistentClient(path="./chroma_db")

        # 获取所有集合的列表
        existing_collections = chroma_client.list_collections()
        logger.debug(f"Questions: {existing_collections}")

        # 检查 "test" 集合是否存在
        if "test" in existing_collections:
            # 存在则加载集合
            self.chroma_collection = chroma_client.get_collection("test",embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                        api_key=self.api_key,
                        api_base=self.api_base,
                        model_name="text-embedding-3-large"
                    ))
            self.is_new_collection = False
        else:
            # 不存在则创建集合
            try:
                self.chroma_collection = chroma_client.create_collection(
                    "test",
                    embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                        api_key=self.api_key,
                        api_base=self.api_base,
                        model_name="text-embedding-3-large"
                    )
                )
                self.is_new_collection = True
            except chromadb.db.base.UniqueConstraintError:
                # 如果尝试创建时出现错误，说明集合已存在
                self.chroma_collection = chroma_client.get_collection("test",embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                        api_key=self.api_key,
                        api_base=self.api_base,
                        model_name="text-embedding-3-large"
                    ))
                self.is_new_collection = False

    def create_vector_store(self, md_contents, meta_data):
        # Process Markdown content and store it in Chroma
        if self.is_new_collection:  # 仅当是新集合时执行
            # 确保 ids 的长度与 md_contents 和 meta_data 中较短的一方相匹配
            min_length = min(len(md_contents), len(meta_data))
            ids = [str(i) for i in range(min_length)]
            # 只使用相应长度的 md_contents 和 meta_data
            self.chroma_collection.add(ids=ids, documents=md_contents[:min_length], metadatas=meta_data[:min_length])
        else:
            logger.debug(f"judge: {self.is_new_collection}")



if __name__ == "__main__":
    test = ChromaManager(api_key="", api_base="")
