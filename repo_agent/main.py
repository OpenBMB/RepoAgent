import typer
from typing import List, Optional
from typing_extensions import Annotated
from repo_agent.config import settings, export_settings, validate_settings
from pathlib import Path
from repo_agent.runner import Runner
from loguru import logger

app = typer.Typer()

@app.command()
def run():
    errors = validate_settings()
    if errors:
        typer.echo(f"Configuration validation failed with errors: {errors}")
        raise typer.Exit(code=1)
    
    try:
        runner = Runner()
        runner.run()
        logger.info("文档任务完成。")
    except Exception as e:
        logger.error(f"运行过程中出现错误: {e}")
        raise typer.Exit(code=1)
    
@app.command()
def configure(
    repo_path: Annotated[str, typer.Option(prompt="Enter the path to your local repository")] = settings.repo_path ,
    model: Annotated[str, typer.Option(prompt="Enter the model name(recommended: gpt-3.5-turbo-16k)")] = settings.chat_completion_kwargs.model,
    base_url: Annotated[str, typer.Option(prompt="Enter the base url of model")] = settings.chat_completion_kwargs.base_url,
    temperature: Annotated[float, typer.Option(prompt="Enter the temperature of model")] = settings.chat_completion_kwargs.temperature,
    request_timeout: Annotated[int, typer.Option(prompt="Enter the request timeout of model")] = settings.chat_completion_kwargs.request_timeout,
    project_hierarchy_path: Annotated[str, typer.Option(prompt="Enter the project hierarchy file name")] = settings.project_hierarchy_path,
    markdown_docs_path: Annotated[str, typer.Option(prompt="Enter the Markdown documents folder name")] = settings.markdown_docs_path,
    language: Annotated[str, typer.Option(prompt="Enter the language option for the docs")] = settings.language,
    # TODO Use ignore_list to ignore files or directories
    #ignore_list: Annotated[Optional[List[str]], typer.Option(prompt="Enter files or directories to ignore")] = settings.ignore_list,
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
    #settings.ignore_list = ignore_list

    errors = validate_settings()
    if errors:
        typer.echo(f"Configuration validation failed with errors: {errors}")
        raise typer.Exit(code=1)

    export_settings()
    typer.echo("Configuration updated and saved.")

