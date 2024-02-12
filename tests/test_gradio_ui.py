import unittest
from unittest.mock import patch, MagicMock
from ..repo_agent.chat_with_repo.gradio_interface import GradioInterface  # Replace 'your_module' with the actual module name

class TestGradioInterface(unittest.TestCase):

    def setUp(self):
        self.mock_respond_function = MagicMock()
        self.gradio_interface = GradioInterface(self.mock_respond_function)

    @patch('gradio.Blocks')
    def test_setup_gradio_interface(self, MockBlocks):
        # Test the setup of the Gradio interface
        self.gradio_interface.setup_gradio_interface()
        MockBlocks.assert_called()

    def test_respond_function_integration(self):
        # Ensure the respond function is integrated and called correctly
        test_msg = "Hello"
        test_system = "System Message"
        self.gradio_interface.respond(test_msg, test_system)
        self.mock_respond_function.assert_called_with(test_msg, test_system)

if __name__ == '__main__':
    unittest.main()
