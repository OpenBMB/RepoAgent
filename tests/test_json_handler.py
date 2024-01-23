import unittest
from unittest.mock import patch, mock_open
from ..repo_agent.chat_with_repo.json_handler import JsonFileProcessor  # Adjust the import according to your project structure

class TestJsonFileProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = JsonFileProcessor("test.json")

    @patch("builtins.open", new_callable=mock_open, read_data='{"files": [{"objects": [{"md_content": "content1"}]}]}')
    def test_read_json_file(self, mock_file):
        # Test read_json_file method
        data = self.processor.read_json_file()
        self.assertEqual(data, {"files": [{"objects": [{"md_content": "content1"}]}]})
        mock_file.assert_called_with("test.json", "r", encoding="utf-8")

    @patch.object(JsonFileProcessor, 'read_json_file')
    def test_extract_md_contents(self, mock_read_json):
        # Test extract_md_contents method
        mock_read_json.return_value = {"files": [{"objects": [{"md_content": "content1"}]}]}
        md_contents = self.processor.extract_md_contents()
        self.assertIn("content1", md_contents)

    @patch("builtins.open", new_callable=mock_open, read_data='{"name": "test", "files": [{"name": "file1"}]}')
    def test_search_in_json_nested(self, mock_file):
        # Test search_in_json_nested method
        result = self.processor.search_in_json_nested("test.json", "file1")
        self.assertEqual(result, {"name": "file1"})
        mock_file.assert_called_with("test.json", "r", encoding="utf-8")

    # Additional tests for error handling (FileNotFoundError, JSONDecodeError, etc.) can be added here

if __name__ == '__main__':
    unittest.main()
