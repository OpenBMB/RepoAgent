from pydantic_settings import BaseSettings
from pydantic import (
    PositiveFloat,
    HttpUrl,
    PositiveInt,
    DirectoryPath,
    SecretStr,
    field_validator,
    field_serializer,
    Field,
)
from repo_agent.config_manager import read_config, write_config
from iso639 import Language, LanguageNotFoundError
from repo_agent.log import LogLevel, set_logger_level_from_config

class ProjectSettings(BaseSettings):
    target_repo: DirectoryPath = ""
    hierarchy_name: str = ".project_doc_record"
    markdown_docs_name: str = "markdown_docs"
    ignore_list: list[str] = []
    language: str = "Chinese"
    max_thread_count: PositiveInt = 4
    max_document_tokens: PositiveInt = 1024
    log_level: LogLevel = Field(default=LogLevel.INFO)

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
        
    @field_validator("log_level", mode='before')
    @classmethod
    def set_log_level(cls, v: str) -> LogLevel:
            if isinstance(v, str):
                v = v.upper()  # 将输入转换为大写
            if v in LogLevel._value2member_map_:  # 检查转换后的值是否在枚举成员中
                return LogLevel(v)
            raise ValueError(f'Invalid log level: {v}')

    @field_serializer('target_repo')
    def serialize_target_repo(self, target_repo: DirectoryPath):
        return str(target_repo)

class ChatCompletionSettings(BaseSettings):
    model: str = "gpt-3.5-turbo"
    temperature: PositiveFloat = 0.2
    request_timeout: PositiveInt = 60
    base_url: HttpUrl = "https://api.openai.com/v1"
    openai_api_key: SecretStr = Field(..., exclude=True)


    @field_serializer('base_url')
    def serialize_base_url(self, base_url: HttpUrl):
        return str(base_url)
    
class Setting(BaseSettings):
    project: ProjectSettings = {}
    chat_completion: ChatCompletionSettings = {}


_config_data = read_config()
setting = Setting.model_validate(_config_data)
set_logger_level_from_config(log_level=setting.project.log_level)

if _config_data == {}:
    write_config(setting.model_dump())