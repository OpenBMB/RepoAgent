import yaml
import sys

try:
    CONFIG = yaml.load(open("config.yml", "r"), Loader=yaml.FullLoader)
except FileNotFoundError:
    print(
        "The file does not exist! Maybe you forgot to rename config.yml.template to config.yml and update the essential content"
    )
    sys.exit(1)  # Exits the program

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
