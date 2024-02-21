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

# 获取 yaml 文件中实际使用的模型列表
used_models = []
for model_name, _ in CONFIG['api_keys'].items():
    used_models.append(model_name)

# NOTE Each model's token limit has been reduced by 1024 tokens to account for the output space and 1 for boundary conditions.
max_input_tokens_map = {
    "gpt-3.5-turbo": 4096, # NOTE OPENAI said that The gpt-3.5-turbo model alias will be automatically upgraded from gpt-3.5-turbo-0613 to gpt-3.5-turbo-0125 on February 16th. But in 2/20, then still maintain 4,096 tokens for context window.
    "gpt-3.5-turbo-0613": 4096, # NOTE Will be deprecated on June 13, 2024.
    "gpt-3.5-turbo-16k": 16384, # NOTE Will be deprecated on June 13, 2024.
    "gpt-3.5-turbo-16k-0613": 16384, # NOTE Will be deprecated on June 13, 2024.
    "gpt-3.5-turbo-0125": 16384,
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-32k": 32768, # NOTE This model was never rolled out widely in favor of GPT-4 Turbo.
    "gpt-4-1106": 131072,
    "gpt-4-0125-preview": 131072,
    "gpt-4-turbo-preview": 131072,
}

# 移除在 yaml 文件中未使用的模型
for model_key in list(max_input_tokens_map.keys()):
    if model_key not in used_models:
        del max_input_tokens_map[model_key]

