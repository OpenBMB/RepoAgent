import pytest
from pydantic_settings import BaseSettings
from repo_agent.config_manager import read_config
from repo_agent.settings import ProjectSettings, ChatCompletionKwargsSettings, Setting
import os


# 示例配置数据
SAMPLE_CONFIG_DATA = {
    "project": {
        "repo_path": "/path/to/repo",
        "project_hierarchy_path": "/path/to/hierarchy",
        "markdown_docs_path": "/path/to/docs",
        "ignore_list": ["file1", "file2"],
        "language": "en"
    },
    "chat_completion_kwargs": {
        "model": "gpt-3",
        "temperature": 0.7,
        "request_timeout": 30,
        "base_url": "http://api.example.com",
        "api_key": "your_api_key"
    }
}

def test_valid_project_settings():
    settings = ProjectSettings(**SAMPLE_CONFIG_DATA["project"])
    assert settings.repo_path == "/path/to/repo"
    # ... 其他字段的断言

def test_invalid_project_settings():
    with pytest.raises(ValueError):
        # 提供不完整或无效的配置数据
        ProjectSettings(**{"repo_path": "/path/to/repo"})

def test_valid_chat_completion_kwargs_settings():
    settings = ChatCompletionKwargsSettings(**SAMPLE_CONFIG_DATA["chat_completion_kwargs"])
    assert settings.model == "gpt-3"
    # ... 其他字段的断言

def test_invalid_chat_completion_kwargs_settings():
    with pytest.raises(ValueError):
        # 提供不完整或无效的配置数据
        ChatCompletionKwargsSettings(**{"model": "gpt-3"})

def test_env_override():
    # 设置环境变量以覆盖配置
    os.environ["repoagent_api_key"] = "new_api_key"
    settings = ChatCompletionKwargsSettings(**SAMPLE_CONFIG_DATA["chat_completion_kwargs"])
    assert settings.api_key == "new_api_key"
