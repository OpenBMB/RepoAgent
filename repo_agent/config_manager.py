import yaml

CONFIG = yaml.load(open("config.yml", "r"), Loader=yaml.FullLoader)

language_mapping = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ru": "Russian",
    "it": "Italian",
    "ko": "Korean",
    "nl": "Dutch",
    "pt": "Portuguese",
    "ar": "Arabic",
    "tr": "Turkish",
    "sv": "Swedish",
    "da": "Danish",
    "fi": "Finnish",
    "no": "Norwegian",
    "pl": "Polish",
    "cs": "Czech",
    "hu": "Hungarian",
    "el": "Greek",
    "he": "Hebrew",
    "th": "Thai",
    "hi": "Hindi",
    "bn": "Bengali",
}

# repo_agent/config_manager.py
import sys
from tomlkit.toml_file import TOMLFile, TOMLDocument
from loguru import logger

_config_file_path = "config.toml"


def read_config(file_path: str = _config_file_path) -> TOMLDocument:
    """
    Reads the TOML configuration file.

    Args:
        file_path (str): The file path to the TOML configuration file.

    Returns:
        TOMLDocument: The configuration data from the TOML file.

    Raises:
        SystemExit: If the file is not found.
    """
    try:
        toml_file = TOMLFile(file_path)
        return toml_file.read()
    except FileNotFoundError:
        logger.error("Configuration file not found.")
        sys.exit(1)


def write_config(
    update_config: TOMLDocument, file_path: str = _config_file_path
) -> None:
    """
    Updates specific sections of the configuration in the TOML file.

    Args:
        update_config (dict): A dictionary containing the sections and values to update.
        file_path (str): The file path to the TOML configuration file.

    Raises:
        SystemExit: If there is an error writing to the file.
    """
    try:
        toml_file = TOMLFile(file_path)
        existing_config = toml_file.read()

        # Iterate through the specific sections in update_config
        for section in update_config:
            if section in existing_config:
                existing_config[section].update(update_config[section])

        toml_file.write(existing_config)
        logger.success("Configuration updated successfully.")
    except Exception as e:
        logger.error(f"Error writing to the configuration file: {e}")
        sys.exit(1)


def update_config_section(config: dict, section: str, updates: dict) -> None:
    """
    Update a specific section of the configuration in memory.

    Args:
        config (dict): The configuration dictionary containing all configuration items.
        section (str): The name of the section to update within the configuration.
        updates (dict): A dictionary containing the updates, where keys are the names of the configuration items and values are the new values for these items.

    Returns:
        None: This function does not return anything. It updates the `config` dictionary in place.
    """
    config_section = config.get(section, {})
    for key, value in updates.items():
        if value is not None:
            config_section[key] = value
    config[section] = config_section


config = read_config()
