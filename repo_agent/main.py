import click
from repo_agent.settings import (
    Setting,
    ProjectSettings,
    ChatCompletionSettings,
)
from repo_agent.config_manager import write_config
from importlib import metadata
from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    retry_if_exception_type,
    stop_after_attempt,
)
from iso639 import Language, LanguageNotFoundError
from repo_agent.log import LogLevel

# 尝试获取版本号，如果失败，则使用默认版本号。
try:
    version_number = metadata.version("repoagent")
except metadata.PackageNotFoundError:
    version_number = "0.0.0"

project_settings_default_instance = ProjectSettings()
chat_completion_default_instance = ChatCompletionSettings()


@retry(
    retry=retry_if_exception_type(LanguageNotFoundError),
    stop=stop_after_attempt(3),
    retry_error_callback=lambda _: click.echo(
        "Failed to find the language after several attempts."
    ),
)
def language_prompt(default_language):
    language_code = click.prompt(
        "Enter the language (ISO 639 code or language name, e.g., 'en', 'eng', 'English')",
        default=default_language,
    )
    try:
        language_name = Language.match(language_code).name
        return language_name
    except LanguageNotFoundError:
        click.echo(
            "Invalid language input. Please enter a valid ISO 639 code or language name."
        )
        raise


@click.group()
@click.version_option(version_number)
def cli():
    """An LLM-powered repository agent designed to assist developers and teams in generating documentation and understanding repositories quickly."""
    pass


@cli.command()
def configure():
    """Configure the agent's parameters."""
    project_settings_instance = ProjectSettings(
        target_repo=click.prompt(
            "Enter the path to target repository",
            type=click.Path(exists=True, file_okay=False, dir_okay=True),
        ),
        hierarchy_name=click.prompt(
            "Enter the project hierarchy file name",
            default=project_settings_default_instance.hierarchy_name,
        ),
        markdown_docs_name=click.prompt(
            "Enter the Markdown documents folder name",
            default=project_settings_default_instance.markdown_docs_name,
        ),
        ignore_list=click.prompt(
            "Enter files or directories to ignore, separated by commas",
            default=",".join(project_settings_default_instance.ignore_list),
        ).split(","),
        language=language_prompt(
            default_language=project_settings_default_instance.language
        ),
        max_thread_count=click.prompt(
            "Enter the maximum number of threads",
            default=project_settings_default_instance.max_thread_count,
            type=click.INT,
        ),
        max_document_tokens=click.prompt(
            "Enter the maximum number of document tokens",
            default=project_settings_default_instance.max_document_tokens,
            type=click.INT,
        ),
        log_level=click.prompt(
            "Enter the log level",
            type=click.Choice(
                [level.value for level in LogLevel], case_sensitive=False
            ),
            default=project_settings_default_instance.log_level.value,
        ),
    )

    logger.info("Project settings saved successfully.")

    chat_completion_instance = ChatCompletionSettings(
        model=click.prompt(
            "Enter the model", default=chat_completion_default_instance.model
        ),
        temperature=click.prompt(
            "Enter the temperature",
            default=chat_completion_default_instance.temperature,
            type=float,
        ),
        request_timeout=click.prompt(
            "Enter the request timeout (seconds)",
            default=chat_completion_default_instance.request_timeout,
            type=int,
        ),
        base_url=click.prompt(
            "Enter the base URL", default=str(chat_completion_default_instance.base_url)
        ),
    )
    logger.info("Chat completion settings saved successfully.")

    update_setting = Setting(
        project=project_settings_instance, chat_completion=chat_completion_instance
    )

    logger.debug(f"Current settings: {update_setting.model_dump()}")

    write_config(update_setting.model_dump())


@cli.command()
@click.option(
    "--model",
    "-m",
    default=chat_completion_default_instance.model,
    show_default=True,
    help="Specifies the model to use for completion.",
    type=str,
)
@click.option(
    "--temperature",
    "-t",
    default=chat_completion_default_instance.temperature,
    show_default=True,
    help="Sets the generation temperature for the model. Lower values make the model more deterministic.",
    type=float,
)
@click.option(
    "--request-timeout",
    "-r",
    default=chat_completion_default_instance.request_timeout,
    show_default=True,
    help="Defines the timeout in seconds for the API request.",
    type=int,
)
@click.option(
    "--base-url",
    "-b",
    default=chat_completion_default_instance.base_url,
    show_default=True,
    help="The base URL for the API calls.",
    type=str,
)
@click.option(
    "--target-repo-path",
    "-tp",
    default=project_settings_default_instance.target_repo,
    show_default=True,
    help="The file system path to the target repository. This path is used as the root for documentation generation.",
    type=click.Path(),
)
@click.option(
    "--hierarchy-path",
    "-hp",
    default=project_settings_default_instance.hierarchy_name,
    show_default=True,
    help="The name or path for the project hierarchy file, used to organize documentation structure.",
    type=str,
)
@click.option(
    "--markdown-docs-path",
    "-mdp",
    default=project_settings_default_instance.markdown_docs_name,
    show_default=True,
    help="The folder path where Markdown documentation will be stored or generated.",
    type=str,
)
@click.option(
    "--ignore-list",
    "-i",
    default=project_settings_default_instance.ignore_list,
    show_default=True,
    help="A list of files or directories to ignore during documentation generation, separated by commas.",
    multiple=True,
    type=str,
)
@click.option(
    "--language",
    "-l",
    default=project_settings_default_instance.language,
    show_default=True,
    help="The ISO 639 code or language name for the documentation. ",
    type=str,
)
@click.option(
    "--log-level",
    "-ll",
    default=project_settings_default_instance.log_level,
    show_default=True,
    help="Sets the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL) for the application. Default is INFO.",
    type=click.Choice([level.value for level in LogLevel], case_sensitive=False),
)
def run(
    model,
    temperature,
    request_timeout,
    base_url,
    target_repo_path,
    hierarchy_path,
    markdown_docs_path,
    ignore_list,
    language,
    log_level,
):
    """Run the program with the specified parameters."""

    project_settings = ProjectSettings(
        target_repo=target_repo_path,
        hierarchy_name=hierarchy_path,
        markdown_docs_name=markdown_docs_path,
        ignore_list=list(ignore_list),  # convert tuple from 'multiple' option to list
        language=language,
        log_level=log_level,
    )

    chat_completion_settings = ChatCompletionSettings(
        model=model,
        temperature=temperature,
        request_timeout=request_timeout,
        base_url=base_url,
    )

    settings = Setting(
        project=project_settings, chat_completion=chat_completion_settings
    )
    write_config(settings.model_dump())


if __name__ == "__main__":
    cli()
