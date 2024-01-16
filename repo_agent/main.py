import click
from repo_agent.config_manager import (
    write_config,
    read_config,
    update_config_section,
)
from importlib import metadata
from repo_agent.runner import Runner
from loguru import logger
from tenacity import (
    retry,
    stop_after_attempt,
    retry_if_exception_type,
    stop_after_attempt,
)
from iso639 import Language, LanguageNotFoundError


# 尝试获取版本号，如果失败，则使用默认版本号。
try:
    version_number = metadata.version("repoagent")
except metadata.PackageNotFoundError:
    version_number = "0.0.0"


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
    """This tool helps you to configure and run tasks."""
    pass


@cli.command()
def configure():
    """Configure the tool's parameters."""

    config = read_config()

    # Project configuration
    config["project"] = {
        "target_repo_path": click.prompt(
            "Enter the path to target repository",
            show_default=False,
            default=config.get("repo_path", ""),
        ),
        "hierarchy_path": click.prompt(
            "Enter the project hierarchy file name",
            default=config.get("hierarchy_path", ".project_hierarchy_path.json"),
        ),
        "markdown_docs_path": click.prompt(
            "Enter the Markdown documents folder name",
            default=config.get("markdown_docs_path", "markdown_docs"),
        ),
        "ignore_list": click.prompt(
            "Enter files/directories to ignore",
            default=config.get(
                "ignore_list", "ignore_file1.py ignore_file2.py ignore_directory"
            ),
        ).split(),
        "language": language_prompt(default_language=config.get("language", "zh")),
    }

    # Chat completion kwargs configuration
    config["chat_completion_kwargs"] = {
        "model": click.prompt(
            "Enter the model name", default=config.get("model", "gpt-3.5-turbo")
        ),
        "temperature": click.prompt(
            "Enter the temperature of model",
            default=config.get("temperature", 0.2),
            type=float,
        ),
        "request_timeout": click.prompt(
            "Enter the request timeout of model",
            default=config.get("request_timeout", 60),
            type=int,
        ),
        "base_url": click.prompt(
            "Enter the base url of model",
            default=config.get("base_url", "https://api.openai.com/v1"),
        ),
    }

    write_config(config)


@cli.command()
@click.option("--model", "-m", help="Model to use", type=str)
@click.option("--temperature", "-t", help="Temperature for the model", type=float)
@click.option("--request-timeout", help="Request timeout", type=int)
@click.option("--base-url", help="Base URL for the API", type=str)
@click.option("--target-repo-path", help="Path to target repository", type=str)
@click.option("--hierarchy-path", help="Project hierarchy file path", type=str)
@click.option("--markdown-docs-path", help="Markdown documents folder path", type=str)
@click.option("--ignore-list", help="Files/directories to ignore", multiple=True)
@click.option("--language", help="Language option for the docs", type=str)
def run(**kwargs):
    """Run a task with the current configuration."""

    # 提取出 chat_completion_kwargs 和 project 相关的参数
    chat_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k in ["model", "temperature", "request_timeout", "base_url"]
    }
    project_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k
        in [
            "repo_path",
            "project_hierarchy_path",
            "markdown_docs_path",
            "ignore_list",
            "language",
        ]
    }

    config = read_config()

    update_config_section(config, "chat_completion_kwargs", chat_kwargs)
    update_config_section(config, "project", project_kwargs)

    write_config(config)

    runner = Runner()

    runner.run()

    logger.info("文档任务完成。")


if __name__ == "__main__":
    cli()
