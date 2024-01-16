from pydantic_settings import BaseSettings, SettingsConfigDict
from config_manager import read_config


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    target_repo_path: str = ""
    hierarchy_path: str
    markdown_docs_path: str
    ignore_list: list[str]
    language: str


class ChatCompletionKwargsSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_prefix="repoagent_")

    model: str
    temperature: float
    request_timeout: int
    base_url: str
    api_key: str


class Setting(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    project: ProjectSettings
    chat_completion_kwargs: ChatCompletionKwargsSettings


_config_data = read_config()
setting = Setting.model_validate(_config_data)
