from repo_agent.chat_with_repo.gradio_ui import GradioInterface
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
    log_file = config['log_file']
    assistant = RepoAssistant(api_key, api_base, db_path,log_file)
    md_contents = assistant.json_data.extract_md_contents()
    assistant.chroma_data.create_vector_store(md_contents)
    GradioInterface(assistant.respond)

    
if __name__ == "__main__":
    main()
