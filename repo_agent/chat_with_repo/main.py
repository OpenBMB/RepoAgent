from repo_agent.chat_with_repo.gradio_interface import GradioInterface
from repo_agent.chat_with_repo.rag import RepoAssistant
from repo_agent.settings import setting


def main():
    api_key = setting.chat_completion.openai_api_key.get_secret_value()
    api_base = str(setting.chat_completion.base_url)
    db_path = (
        setting.project.target_repo
        / setting.project.hierarchy_name
        / "project_hierarchy.json"
    )

    assistant = RepoAssistant(api_key, api_base, db_path)
    md_contents, meta_data = assistant.json_data.extract_data()
    assistant.chroma_data.create_vector_store(md_contents, meta_data)
    GradioInterface(assistant.respond)


if __name__ == "__main__":
    main()
