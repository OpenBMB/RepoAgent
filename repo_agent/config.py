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
