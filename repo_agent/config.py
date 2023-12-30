import yaml

CONFIG = yaml.load(open('config.yml', 'r'), Loader=yaml.FullLoader)

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
    "bn": "Bengali"
}

class ConfigManager:
    def __init__(self, file_path='config.yml'):
        self.file_path = file_path
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.file_path, 'r') as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            return {}

    def update_partial_config(self, section, updates):
        self.config[section] = {**self.config.get(section, {}), **updates}
        self.save_config()

    def save_config(self):
        with open(self.file_path, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)
