from pydantic_settings import BaseSettings, SettingsConfigDict
from repo_agent.config_manager import read_config


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


class LazySettings:
    """
    A settings manager that lazily loads configuration data.

    The configuration is only loaded once when any attribute of the settings
    manager is accessed for the first time. Subsequent attribute accesses will
    use the already loaded configuration.

    Attributes:
        _settings: Internal storage for the loaded settings.
    """

    _settings = None

    def __getattr__(self, item):
        """
        Override the method to access attributes.

        If the settings have not been loaded yet, it triggers the loading
        process. Once the settings are loaded, it returns the requested
        attribute if it exists.

        Args:
            item: The name of the attribute being accessed.

        Returns:
            The value of the requested attribute from the settings.

        Raises:
            AttributeError: If the attribute does not exist in the settings.
        """
        if self._settings is None:
            self._settings = self._load_settings()
        try:
            return getattr(self._settings, item)
        except AttributeError as e:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'") from e

    @staticmethod
    def _load_settings():
        """
        Load the settings from the configuration file.

        This method uses the 'read_config' function to read the configuration
        data and then validates it using the 'Setting' class's 'model_validate' method.

        Returns:
            The validated settings object.

        Raises:
            Any exceptions raised by 'read_config' or 'Setting.model_validate'.
        """
        _config_data = read_config()
        return Setting.model_validate(_config_data)


# Instance of LazySettings to be used throughout the application.
setting = LazySettings()
