import os
from repo_agent.chat_with_repo.gradio_interface import GradioInterface
from repo_agent.chat_with_repo.rag import RepoAssistant
from repo_agent.config import CONFIG


def main():
    _model = CONFIG["default_completion_kwargs"]["model"]
    api_key = CONFIG["api_keys"][_model][0]["api_key"]
    api_base = CONFIG["api_keys"][_model][0]["base_url"]
    db_path = os.path.join(
        CONFIG["repo_path"], CONFIG["project_hierarchy"], "project_hierarchy.json"
    )

    assistant = RepoAssistant(api_key, api_base, db_path)
    md_contents = assistant.json_data.extract_md_contents()
    meta_data = assistant.json_data.extract_metadata()
    assistant.chroma_data.create_vector_store(md_contents, meta_data)
    GradioInterface(assistant.respond)


if __name__ == "__main__":
    main()
