from enum import StrEnum
from typing import List, Optional

from iso639 import Language, LanguageNotFoundError
from pydantic import (
    BaseModel,
    ConfigDict,
    DirectoryPath,
    Field,
    HttpUrl,
    PositiveFloat,
    PositiveInt,
    SecretStr,
    field_validator,
)
from pydantic_settings import BaseSettings


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
    # NOTE: Temporarily disabling the limit on prompt tokens as the model context window is sufficiently large
    # max_document_tokens: PositiveInt = 16384
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


class MaxInputTokens(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    gpt_4o_mini: int = Field(128000, alias="gpt-4o-mini")  # type: ignore
    gpt_4o: int = Field(128000, alias="gpt-4o")  # type: ignore
    o1_preview: int = Field(128000, alias="o1-preview")  # type: ignore
    o1_mini: int = Field(128000, alias="o1-mini")  # type: ignore
    glm_4_flash: int = Field(128000, alias="glm-4-flash")  # type: ignore

    @classmethod
    def get_valid_models(cls) -> List[str]:
        # Use model_fields to get all field aliases or names
        return [
            field.alias if field.alias else name
            for name, field in cls.model_fields.items()
        ]

    @classmethod
    def get_token_limit(cls, model_name: str) -> int:
        instance = cls()
        return getattr(instance, model_name.replace("-", "_"))


class ChatCompletionSettings(BaseSettings):
    model: str = "gpt-4o-mini"
    temperature: PositiveFloat = 0.2
    request_timeout: PositiveInt = 60
    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key: SecretStr = Field(..., exclude=True)

    @field_validator("openai_base_url", mode="before")
    @classmethod
    def convert_base_url_to_str(cls, openai_base_url: HttpUrl) -> str:
        return str(openai_base_url)

    @field_validator("model")
    @classmethod
    def validate_model(cls, value: str) -> str:
        valid_models = MaxInputTokens.get_valid_models()
        if value not in valid_models:
            raise ValueError(f"Invalid model '{value}'. Must be one of {valid_models}.")
        return value

    def get_token_limit(self) -> int:
        # Retrieve the token limit based on the model value
        return MaxInputTokens.get_token_limit(self.model)


class Setting(BaseSettings):
    project: ProjectSettings = {}  # type: ignore
    chat_completion: ChatCompletionSettings = {}  # type: ignore


class SettingsManager:
    _setting_instance: Optional[Setting] = (
        None  # Private class attribute, initially None
    )

    @classmethod
    def get_setting(cls):
        if cls._setting_instance is None:  # Check if it has been initialized
            cls._setting_instance = Setting()  # Initialize the setting object
        return cls._setting_instance  # Return the setting object


if __name__ == "__main__":
    setting = SettingsManager.get_setting()
    print(setting.model_dump())
