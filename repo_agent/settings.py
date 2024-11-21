from enum import StrEnum
from typing import Optional

from iso639 import Language, LanguageNotFoundError
from pydantic import (
    DirectoryPath,
    Field,
    HttpUrl,
    PositiveFloat,
    PositiveInt,
    SecretStr,
    field_validator,
)
from pydantic_settings import BaseSettings
from pathlib import Path


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
    language: str = "English"
    max_thread_count: PositiveInt = 4
    log_level: LogLevel = LogLevel.INFO

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
            v = v.upper()  # Convert input to uppercase
        if (
            v in LogLevel._value2member_map_
        ):  # Check if the converted value is in enum members
            return LogLevel(v)
        raise ValueError(f"Invalid log level: {v}")


class ChatCompletionSettings(BaseSettings):
    model: str = "gpt-4o-mini"  # NOTE: No model restrictions for user flexibility, but it's recommended to use models with a larger context window.
    temperature: PositiveFloat = 0.2
    request_timeout: PositiveInt = 60
    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key: SecretStr = Field(..., exclude=True)

    @field_validator("openai_base_url", mode="before")
    @classmethod
    def convert_base_url_to_str(cls, openai_base_url: HttpUrl) -> str:
        return str(openai_base_url)


class Setting(BaseSettings):
    project: ProjectSettings = {}  # type: ignore
    chat_completion: ChatCompletionSettings = {}  # type: ignore


class SettingsManager:
    _setting_instance: Optional[Setting] = (
        None  # Private class attribute, initially None
    )

    @classmethod
    def get_setting(cls):
        if cls._setting_instance is None:
            cls._setting_instance = Setting()
        return cls._setting_instance

    @classmethod
    def initialize_with_params(
        cls,
        target_repo: Path,
        markdown_docs_name: str,
        hierarchy_name: str,
        ignore_list: list[str],
        language: str,
        max_thread_count: int,
        log_level: str,
        model: str,
        temperature: float,
        request_timeout: int,
        openai_base_url: str,
    ):
        project_settings = ProjectSettings(
            target_repo=target_repo,
            hierarchy_name=hierarchy_name,
            markdown_docs_name=markdown_docs_name,
            ignore_list=ignore_list,
            language=language,
            max_thread_count=max_thread_count,
            log_level=LogLevel(log_level),
        )

        chat_completion_settings = ChatCompletionSettings(
            model=model,
            temperature=temperature,
            request_timeout=request_timeout,
            openai_base_url=openai_base_url,
        )

        cls._setting_instance = Setting(
            project=project_settings,
            chat_completion=chat_completion_settings,
        )


if __name__ == "__main__":
    setting = SettingsManager.get_setting()
    print(setting.model_dump())
