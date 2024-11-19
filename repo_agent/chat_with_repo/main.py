import time

from repo_agent.chat_with_repo.gradio_interface import GradioInterface
from repo_agent.chat_with_repo.rag import RepoAssistant
from repo_agent.log import logger
from repo_agent.settings import SettingsManager


def main():
    logger.info("Initializing the RepoAgent chat with doc module.")

    # Load settings
    setting = SettingsManager.get_setting()

    api_key = setting.chat_completion.openai_api_key.get_secret_value()
    api_base = str(setting.chat_completion.openai_base_url)
    db_path = (
        setting.project.target_repo
        / setting.project.hierarchy_name
        / "project_hierarchy.json"
    )

    # Initialize RepoAssistant
    assistant = RepoAssistant(api_key, api_base, db_path)

    # Extract data
    md_contents, meta_data = assistant.json_data.extract_data()

    # Create vector store and measure runtime
    logger.info("Starting vector store creation...")
    start_time = time.time()
    assistant.vector_store_manager.create_vector_store(
        md_contents, meta_data, api_key, api_base
    )
    elapsed_time = time.time() - start_time
    logger.info(f"Vector store created successfully in {elapsed_time:.2f} seconds.")

    # Launch Gradio interface
    GradioInterface(assistant.respond)


if __name__ == "__main__":
    main()
