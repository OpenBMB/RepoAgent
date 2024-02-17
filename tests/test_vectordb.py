import unittest
from unittest.mock import patch, MagicMock
import chromadb
from ..repo_agent.chat_with_repo.vectordb import ChromaManager  # Replace 'your_module' with the actual module name

class TestChromaManager(unittest.TestCase):

    @patch('chromadb.Client')
    def setUp(self, MockClient):
        # Setup Mock for ChromaDB Client
        self.mock_client = MockClient.return_value
        self.mock_collection = MagicMock()
        self.mock_client.create_collection.return_value = self.mock_collection
        self.mock_client.get_collection.return_value = self.mock_collection

        self.chroma_manager = ChromaManager(api_key="dummy_key", api_base="dummy_base")

    def test_init(self):
        # Test if the object is initialized correctly
        self.assertIsNotNone(self.chroma_manager.chroma_collection)

    def test_init_chroma_collection(self):
        # Test the initialization of chroma collection
        self.chroma_manager.init_chroma_collection()
        self.mock_client.create_collection.assert_called_once()
        self.mock_client.get_collection.assert_called_once()
        self.assertIsNotNone(self.chroma_manager.chroma_collection)

    @patch('chromadb.utils.embedding_functions.OpenAIEmbeddingFunction')
    def test_create_vector_store(self, MockEmbeddingFunction):
        # Test create_vector_store method
        mock_embedding_function = MockEmbeddingFunction.return_value
        mock_embeddings = [0.1, 0.2, 0.3]
        mock_embedding_function.return_value = mock_embeddings

        md_contents = ["doc1", "doc2", "doc3"]
        self.chroma_manager.create_vector_store(md_contents)

        mock_embedding_function.assert_called_with(md_contents)
        self.mock_collection.add.assert_called_with(ids=['0', '1', '2'], documents=md_contents, embeddings=mock_embeddings)

if __name__ == '__main__':
    unittest.main()
