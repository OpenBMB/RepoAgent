import unittest
from unittest.mock import patch, MagicMock
from ..repo_agent.chat_with_repo.rag import RepoAssistant  # Adjust the import according to your project structure

class TestRepoAssistant(unittest.TestCase):

    def setUp(self):
        self.mock_openai = MagicMock()
        self.mock_json_processor = MagicMock()
        self.mock_chroma_manager = MagicMock()
        self.mock_text_analysis_tool = MagicMock()
        self.mock_logger_manager = MagicMock()

        with patch('repo_agent.chat_with_repo.json_handle.JsonFileProcessor', self.mock_json_processor), \
             patch('vectordbs.ChromaManager', self.mock_chroma_manager), \
             patch('prompt.TextAnalysisTool', self.mock_text_analysis_tool), \
             patch('logger.LoggerManager', self.mock_logger_manager), \
             patch('llama_index.llms.OpenAI', self.mock_openai):
            self.assistant = RepoAssistant("api_key", "api_base", "db_path", "log_file")

    def test_generate_queries(self):
        # Test generate_queries method
        self.mock_openai.complete.return_value.text = "Query1\nQuery2\nQuery3"
        queries = self.assistant.generate_queries("test query", 3)
        self.assertEqual(len(queries), 3)

    def test_rag(self):
        # Test rag method
        self.mock_openai.complete.return_value = MagicMock(text="Response")
        response = self.assistant.rag("test query", ["doc1", "doc2"])
        self.assertEqual(response, "Response")

    def test_extract_and_format_documents(self):
        # Test extract_and_format_documents method
        test_results = [{"documents": [["doc1", "doc2"]]}]
        formatted_docs = self.assistant.extract_and_format_documents(test_results)
        self.assertIn("doc1", formatted_docs)
        self.assertIn("doc2", formatted_docs)

    def test_respond(self):
        # Test respond method
        # Set up mock returns for the necessary methods
        self.mock_text_analysis_tool.format_chat_prompt.return_value = "formatted prompt"
        self.mock_text_analysis_tool.keyword.return_value = ["keyword1", "keyword2"]
        self.mock_chroma_manager.chroma_collection.query.return_value = {"documents": [["doc1", "doc2"]]}
        self.mock_openai.complete.return_value = MagicMock(text="Response")

        _, bot_message, _, _, _, _ = self.assistant.respond("test message", "test instruction")
        self.assertIn("Response", bot_message)

if __name__ == '__main__':
    unittest.main()
