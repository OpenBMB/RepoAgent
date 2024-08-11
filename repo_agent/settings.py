import os
from enum import StrEnum
from pathlib import Path

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

from repo_agent.config_manager import write_config
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.joinpath(".env"))


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
    model: str = "gpt-4o-mini"
    temperature: PositiveFloat = 0.2
    request_timeout: PositiveFloat = 60.0
    base_url: HttpUrl = "https://api.openai.com/v1"  # type: ignore
    openai_api_key: SecretStr = Field(os.getenv("OPENAI_API_KEY"), exclude=True)
    huggingface_api_key: SecretStr = Field(os.getenv("HUGGINGFACE_API_TOKEN"), exclude=True)

    @field_serializer("base_url")
    def serialize_base_url(self, base_url: HttpUrl):
        return str(base_url)


class Setting(BaseSettings):
    project: ProjectSettings = {}  # type: ignore
    chat_completion: ChatCompletionSettings = {}  # type: ignore


_config_data = {'project': {
    'target_repo': "",
    'hierarchy_name': '.project_doc_record',
    'markdown_docs_name': "markdown_docs", 'ignore_list': [],
    'language': 'English', 'max_thread_count': 4, 'max_document_tokens': 1024,
    'log_level': 'INFO'}, 'chat_completion': {'model': 'gpt-4o-mini',
                                              'temperature': 0.2,
                                              'request_timeout': 60.0,
                                              'base_url': 'https://api.openai.com/v1'}}
setting = Setting.model_validate(_config_data)

if _config_data == {}:
    write_config(setting.model_dump())