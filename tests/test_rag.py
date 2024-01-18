import unittest
from unittest.mock import patch, MagicMock
from ..repo_agent.chat_with_repo.rag import RepoAssistant  # Adjust the import according to your project structure

class TestRepoAssistant(unittest.TestCase):

    def setUp(self):
        # Mocks for external dependencies
        self.mock_openai = MagicMock()
        self.mock_text_analysis_tool = MagicMock()
        self.mock_json_file_processor = MagicMock()
        self.mock_chroma_manager = MagicMock()

        # Patch the external classes
        self.openai_patch = patch('your_module.OpenAI', return_value=self.mock_openai)
        self.text_analysis_tool_patch = patch('your_module.TextAnalysisTool', return_value=self.mock_text_analysis_tool)
        self.json_file_processor_patch = patch('your_module.JsonFileProcessor', return_value=self.mock_json_file_processor)
        self.chroma_manager_patch = patch('your_module.ChromaManager', return_value=self.mock_chroma_manager)

        # Start the patches
        self.openai_patch.start()
        self.text_analysis_tool_patch.start()
        self.json_file_processor_patch.start()
        self.chroma_manager_patch.start()

        # Initialize RepoAssistant with mocked dependencies
        self.assistant = RepoAssistant("api_key", "api_base", "db_path")
    def tearDown(self):
        # Stop the patches
        self.openai_patch.stop()
        self.text_analysis_tool_patch.stop()
        self.json_file_processor_patch.stop()
        self.chroma_manager_patch.stop()

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
