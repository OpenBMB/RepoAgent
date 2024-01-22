from gradio_ui import GradioInterface
import yaml
from rag import RepoAssistant


def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)
    
    
def main():
    config = load_config("config.yml")
    api_key = config['api_key']
    api_base = config['api_base']
    db_path = config['db_path']
    assistant = RepoAssistant(api_key, api_base, db_path)
    md_contents = assistant.json_data.extract_md_contents()
    meta_data = assistant.json_data.extract_metadata()
    assistant.chroma_data.create_vector_store(md_contents,meta_data)
    GradioInterface(assistant.respond)

    
if __name__ == "__main__":
    main()
