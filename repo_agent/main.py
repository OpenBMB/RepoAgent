import typer
from typing_extensions import Annotated
from repo_agent.config import settings, export_settings, validate_settings
from pathlib import Path
from repo_agent.runner import Runner
from loguru import logger
from importlib import metadata

# 尝试获取版本号，如果失败，则使用默认版本号。
try:
    version_number = metadata.version("repoagent")
except metadata.PackageNotFoundError:
    version_number = "0.0.0"

# 定义版本信息字符串，以便在应用中复用。
version_info = f"RepoAgent (version {version_number})"

app = typer.Typer(help=version_info)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, version: bool = typer.Option(None, "--version", "-v", help="Show version.")):
    if version:
        typer.echo(version_info)
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        # No subcommand was provided, show help
        typer.echo(ctx.get_help())
        raise typer.Exit()
    

@app.command(help="Run the documentation generation task.")
def run():
    errors = validate_settings()
    if errors:
        typer.echo(f"Configuration validation failed with errors: {errors}")
        raise typer.Exit(code=1)

    try:
        runner = Runner()
        runner.run()
        logger.info("Document task completed.")
    except Exception as e:
        logger.error(f"Error occurred during execution: {e}")
        raise typer.Exit(code=1)


@app.command(help="Configure the tool's parameter settings.")
def configure(
        repo_path: Annotated[str, typer.Option(
            "--repo-path", "-rp",
            prompt="Enter the path to your local repository",
            help="The path to your local repository.",
            show_default=False)] = settings.repo_path,
        model: Annotated[str, typer.Option(
            "--model", "-m",
            prompt="Enter the model name",
            help="The name of the model to use."
        )] = settings.chat_completion_kwargs.model,
        base_url: Annotated[str, typer.Option(
            "--base-url", "-b",
            prompt="Enter the base url of model",
            help="The base URL of the model."
        )] = settings.chat_completion_kwargs.base_url,
        temperature: Annotated[float, typer.Option(
            "--temperature", "-t",
            prompt="Enter the temperature of model",
            help="The temperature of the model, affecting the diversity of generated content.")
        ] = settings.chat_completion_kwargs.temperature,
        request_timeout: Annotated[int, typer.Option(
            "--request-timeout", "-rt",
            prompt="Enter the request timeout of model",
            help="The request timeout for the model, in seconds."
        )] = settings.chat_completion_kwargs.request_timeout,
        project_hierarchy_path: Annotated[str, typer.Option(
            "--project-hierarchy-path", "-p",
            prompt="Enter the project hierarchy file name",
            help="The name of the project hierarchy file."
        )] = settings.project_hierarchy_path,
        markdown_docs_path: Annotated[str, typer.Option(
            "--markdown-docs-path", "-md",
            prompt="Enter the Markdown documents folder name",
            help="The folder name for the Markdown documents."
        )] = settings.markdown_docs_path,
        language: Annotated[str, typer.Option(
            "--language", "-l",
            prompt="Enter the language option for the docs",
            help="The language option for the documentation."
        )] = settings.language,
        # TODO: Use ignore_list to ignore files or directories
        # ignore_list: Annotated[Optional[List[str]], typer.Option(
        #     "--ignore-list", "-il",
        #     prompt="Enter files or directories to ignore",
        #     help="List of files or directories to ignore."
        #     )] = settings.ignore_list,
):
    # 转换为 Path 对象并保存
    path_obj = Path(repo_path)
    settings.repo_path = str(path_obj)
    # 更新其他设置
    settings.chat_completion_kwargs.model = model
    settings.chat_completion_kwargs.temperature = temperature
    settings.chat_completion_kwargs.base_url = base_url
    settings.chat_completion_kwargs.request_timeout = request_timeout
    settings.project_hierarchy_path = project_hierarchy_path
    settings.markdown_docs_path = markdown_docs_path
    settings.language = language
    # settings.ignore_list = ignore_list

    errors = validate_settings()
    if errors:
        typer.echo(f"Configuration validation failed with errors: {errors}")
        raise typer.Exit(code=1)

    export_settings()
    typer.echo("Configuration updated and saved.")


