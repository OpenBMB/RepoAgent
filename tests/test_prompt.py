import unittest
from unittest.mock import patch, MagicMock
from ..repo_agent.chat_with_repo.prompt import TextAnalysisTool  # Adjust the import according to your project structure

class TestTextAnalysisTool(unittest.TestCase):
    def setUp(self):
        # Mocks for OpenAI and JsonFileProcessor
        self.mock_llm = MagicMock()
        self.mock_json_processor = MagicMock()

        # Patching the classes
        self.openai_patch = patch('your_module.OpenAI', return_value=self.mock_llm)
        self.json_processor_patch = patch('your_module.JsonFileProcessor', return_value=self.mock_json_processor)

        # Start the patches
        self.openai_patch.start()
        self.json_processor_patch.start()

        # Initialize TextAnalysisTool with mocked dependencies
        self.text_analysis_tool = TextAnalysisTool(self.mock_llm, "db_path")

    def tearDown(self):
        # Stop the patches
        self.openai_patch.stop()
        self.json_processor_patch.stop()
  
    def test_keyword(self):
        self.mock_llm.complete.return_value = "keyword1, keyword2, keyword3"
        keywords = self.text_analysis_tool.keyword("test query")
        self.assertIn("keyword1", keywords)

    def test_tree(self):
        self.mock_llm.complete.return_value = "tree structure"
        tree_structure = self.text_analysis_tool.tree("test query")
        self.assertEqual(tree_structure, "tree structure")

    def test_format_chat_prompt(self):
        formatted_prompt = self.text_analysis_tool.format_chat_prompt("message", "instruction")
        self.assertIn("User: message", formatted_prompt)

    @patch.object(TextAnalysisTool, 'jsonsearch')
    def test_queryblock(self, mock_jsonsearch):
        mock_jsonsearch.search_in_json_nested.return_value = {'code_content': 'test_code'}
        result = self.text_analysis_tool.queryblock("test message")
        self.assertEqual(result, 'test_code')

    def test_nerquery(self):
        self.mock_llm.complete.return_value = "function_name"
        function_name = self.text_analysis_tool.nerquery("test message")
        self.assertEqual(function_name, "function_name")
        self.mock_logger_manager.get_logger().debug.assert_called()

if __name__ == '__main__':
    unittest.main()
