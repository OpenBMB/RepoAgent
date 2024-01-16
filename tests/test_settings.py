# tests/test_settings.py

# tests/test_settings.py

import pytest

# Your mock configuration data
mock_config_data = {
    'project': {
        'target_repo_path': 'mock/path/to/repo',
        'hierarchy_path': 'mock/path/to/hierarchy',
        'markdown_docs_path': 'mock/path/to/markdown_docs',
        'ignore_list': ['mock_ignore_file1.py', 'mock_ignore_file2.py'],
        'language': 'mock_language'
    },
    'chat_completion_kwargs': {
        'model': 'mock_model',
        'temperature': 0.5,
        'request_timeout': 60,
        'base_url': 'mock://api.example.com',
        'api_key': 'mock_api_key'
    }
}

@pytest.fixture
def mock_read_config(mocker):
    # Patch the read_config function to return the mock configuration data
    mocker.patch("repo_agent.config_manager.read_config", return_value=mock_config_data)

@pytest.fixture
def setting(mock_read_config):
    # Delay the import of the setting object until the read_config has been mocked
    from repo_agent.settings import setting
    return setting

# Test that project settings load correctly
def test_project_settings_load_correctly(setting):
    assert hasattr(setting, 'project'), "Config should have 'project'"
    assert setting.project.target_repo_path == 'mock/path/to/repo', "'target_repo_path' should be correct"
    assert setting.project.hierarchy_path == 'mock/path/to/hierarchy', "'hierarchy_path' should be correct"
    assert setting.project.markdown_docs_path == 'mock/path/to/markdown_docs', "'markdown_docs_path' should be correct"
    assert setting.project.ignore_list == ['mock_ignore_file1.py', 'mock_ignore_file2.py'], "'ignore_list' should be correct"
    assert setting.project.language == 'mock_language', "'language' should be correct"

# Test that chat completion kwargs load correctly
def test_chat_completion_kwargs_load_correctly(setting):
    assert hasattr(setting, 'chat_completion_kwargs'), "Config should have 'chat_completion_kwargs'"
    assert setting.chat_completion_kwargs.model == 'mock_model', "'model' should be correct"
    assert setting.chat_completion_kwargs.temperature == 0.5, "'temperature' should be correct"
    assert setting.chat_completion_kwargs.request_timeout == 60, "'request_timeout' should be correct"
    assert setting.chat_completion_kwargs.base_url == 'mock://api.example.com', "'base_url' should be correct"
    assert setting.chat_completion_kwargs.api_key == 'mock_api_key', "'api_key' should be correct"

