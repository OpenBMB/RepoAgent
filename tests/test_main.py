import unittest
from unittest.mock import patch, mock_open, MagicMock
from repo_agent.chat_with_repo.chat_main import main

class TestMainFunction(unittest.TestCase):
    def setUp(self):
        self.config_data = {
            'api_key': '12345',
            'api_base': 'http://api.example.com',
            'db_path': '/path/to/db',
            'log_file': '/path/to/log'
        }
        self.mock_file = mock_open(read_data=yaml.dump(self.config_data))
        self.patcher_open = patch('builtins.open', self.mock_file)
        self.patcher_yaml = patch('yaml.safe_load', return_value=self.config_data)
        self.patcher_repo_assistant = patch('main.RepoAssistant')
        self.patcher_gradio_interface = patch('main.GradioInterface')

        self.patcher_open.start()
        self.patcher_yaml.start()
        self.mock_repo_assistant = self.patcher_repo_assistant.start()
        self.mock_gradio_interface = self.patcher_gradio_interface.start()

    def tearDown(self):
        patch.stopall()

    def test_main_initialization(self):
        # Call the main function
        main.main()
        
        # Check that the file was opened correctly
        self.mock_file.assert_called_with("config.yml", 'r')
        
        # Check that the RepoAssistant was initialized with the correct parameters
        self.mock_repo_assistant.assert_called_with(
            '12345', 'http://api.example.com', '/path/to/db', '/path/to/log'
        )
        
        # Check that the GradioInterface was initialized with the respond function
        self.mock_gradio_interface.assert_called_once()

    def test_main_function_calls(self):
        # Create a mock for the RepoAssistant instance methods
        assistant_instance = self.mock_repo_assistant.return_value
        assistant_instance.json_data.extract_md_contents.return_value = 'md_contents'
        assistant_instance.chroma_data.create_vector_store.return_value = None

        # Call the main function
        main.main()

        # Verify that extract_md_contents was called
        assistant_instance.json_data.extract_md_contents.assert_called_once()

        # Verify that create_vector_store was called with 'md_contents'
        assistant_instance.chroma_data.create_vector_store.assert_called_with('md_contents')


if __name__ == '__main__':
    unittest.main()
