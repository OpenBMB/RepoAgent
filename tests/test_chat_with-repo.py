import unittest
from unittest.mock import patch, MagicMock
import chromadb
from ..repo_agent.chat_with_repo.vectordbs import ChromaManager  # Replace 'your_module' with the actual module name
from ..repo_agent.chat_with_repo.gradio_ui import GradioInterface
from ..repo_agent.chat_with_repo.rag import RepoAssistant
from ..repo_agent.chat_with_repo.json_handle import JsonFileProcessor
from ..repo_agent.chat_with_repo.prompt import TextAnalysisTool  # 
from ..repo_agent.chat_with_repo.logger import LoggerManager
from repo_agent.chat_with_repo import main
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
class TestTextAnalysisTool(unittest.TestCase):

    def setUp(self):
        self.mock_llm = MagicMock()
        self.mock_logger_manager = MagicMock()
        self.mock_json_processor = MagicMock()
        self.text_analysis_tool = TextAnalysisTool(self.mock_llm, self.mock_logger_manager, "test.json")

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

class TestLoggerManager(unittest.TestCase):

    @patch('logging.getLogger')
    @patch('logging.FileHandler')
    def test_logger_initialization(self, mock_file_handler, mock_get_logger):
        # Mocking the FileHandler and Formatter
        mock_formatter = MagicMock()
        mock_file_handler_instance = mock_file_handler.return_value
        mock_file_handler_instance.setFormatter = MagicMock()

        # Create an instance of LoggerManager
        logger_manager = LoggerManager('test.log')

        # Test if getLogger is called with __name__
        mock_get_logger.assert_called_with(__name__)

        # Test if FileHandler is initialized correctly
        mock_file_handler.assert_called_with('test.log', encoding='utf-8')

        # Test if setFormatter is called on the file handler
        mock_file_handler_instance.setFormatter.assert_called()

    def test_get_logger(self):
        logger_manager = LoggerManager('test.log')
        logger = logger_manager.get_logger()
        self.assertIsNotNone(logger)


class TestScript(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="api_key: key\napi_base: base\ndb_path: path\nlog_file: file.log")
    def test_load_config(self, mock_file):
        # Test load_config function
        config = your_script.load_config("config.yml")
        self.assertEqual(config['api_key'], 'key')
        self.assertEqual(config['api_base'], 'base')
        mock_file.assert_called_with("config.yml", 'r')

    @patch('your_script.RepoAssistant')
    @patch('your_script.GradioInterface')
    @patch('your_script.load_config', return_value={'api_key': 'key', 'api_base': 'base', 'db_path': 'path', 'log_file': 'file.log'})
    def test_main(self, mock_load_config, mock_gradio_interface, mock_repo_assistant):
        # Test main function
        your_script.main()
        mock_load_config.assert_called_with("config.yml")
        mock_repo_assistant.assert_called_with('key', 'base', 'path', 'file.log')
        mock_gradio_interface.assert_called()


if __name__ == '__main__':
    unittest.main()
