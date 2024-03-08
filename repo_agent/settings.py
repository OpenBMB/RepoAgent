from enum import StrEnum

from iso639 import Language, LanguageNotFoundError
from pydantic import (
    DirectoryPath,
    Field,
    HttpUrl,
    PositiveFloat,
    PositiveInt,
    SecretStr,
    field_serializer,
    field_validator,
)
from pydantic_settings import BaseSettings

from repo_agent.config_manager import read_config, write_config


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ProjectSettings(BaseSettings):
    target_repo: DirectoryPath = ""  # type: ignore
    hierarchy_name: str = ".project_doc_record"
    markdown_docs_name: str = "markdown_docs"
    ignore_list: list[str] = []
    language: str = "Chinese"
    max_thread_count: PositiveInt = 4
    max_document_tokens: PositiveInt = 1024
    log_level: LogLevel = LogLevel.INFO

    @field_serializer("ignore_list")
    def serialize_ignore_list(self, ignore_list: list[str] = []):
        if ignore_list == [""]:
            self.ignore_list = []  # If the ignore_list is empty, set it to an empty list
            return [] 
        return ignore_list
    
    @field_validator("language")
    @classmethod
    def validate_language_code(cls, v: str) -> str:
        try:
            language_name = Language.match(v).name
            return language_name  # Returning the resolved language name
        except LanguageNotFoundError:
            raise ValueError(
                "Invalid language input. Please enter a valid ISO 639 code or language name."
            )

    @field_validator("log_level", mode="before")
    @classmethod
    def set_log_level(cls, v: str) -> LogLevel:
        if isinstance(v, str):
            v = v.upper()  # 将输入转换为大写
        if v in LogLevel._value2member_map_:  # 检查转换后的值是否在枚举成员中
            return LogLevel(v)
        raise ValueError(f"Invalid log level: {v}")

    @field_serializer("target_repo")
    def serialize_target_repo(self, target_repo: DirectoryPath):
        return str(target_repo)


class ChatCompletionSettings(BaseSettings):
    model: str = "gpt-3.5-turbo"
    temperature: PositiveFloat = 0.2
    request_timeout: PositiveFloat = 60.0
    base_url: HttpUrl = "https://api.openai.com/v1"  # type: ignore
    openai_api_key: SecretStr = Field(..., exclude=True)

    @field_serializer("base_url")
    def serialize_base_url(self, base_url: HttpUrl):
        return str(base_url)


class Setting(BaseSettings):
    project: ProjectSettings = {}  # type: ignore
    chat_completion: ChatCompletionSettings = {}  # type: ignore


_config_data = read_config()
setting = Setting.model_validate(_config_data)

if _config_data == {}:
    write_config(setting.model_dump())

# NOTE Each model's token limit has been reduced by 1024 tokens to account for the output space and 1 for boundary conditions.
max_input_tokens_map = {
    "gpt-3.5-turbo": 4096,  # NOTE OPENAI said that The gpt-3.5-turbo model alias will be automatically upgraded from gpt-3.5-turbo-0613 to gpt-3.5-turbo-0125 on February 16th. But in 2/20, then still maintain 4,096 tokens for context window.
    "gpt-3.5-turbo-0613": 4096,  # NOTE Will be deprecated on June 13, 2024.
    "gpt-3.5-turbo-16k": 16384,  # NOTE Will be deprecated on June 13, 2024.
    "gpt-3.5-turbo-16k-0613": 16384,  # NOTE Will be deprecated on June 13, 2024.
    "gpt-3.5-turbo-0125": 16384,
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768,  # NOTE This model was never rolled out widely in favor of GPT-4 Turbo.
    "gpt-4-1106": 131072,
    "gpt-4-0125-preview": 131072,
    "gpt-4-turbo-preview": 131072,
}
