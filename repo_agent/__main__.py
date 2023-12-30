# RepoAgent/repo_agent/__main__.py
import typer
import yaml
from .config import ConfigManager
from typing import List, Optional
from typing_extensions import Annotated
from loguru import logger

app = typer.Typer()
api_keys_app = typer.Typer(help="Manage API keys.")
add_app = typer.Typer(help="Add a new API key configuration.")
default_completion_app = typer.Typer(help="Manage default completion configurations.")
app.add_typer(api_keys_app, name="api-keys")
api_keys_app.add_typer(add_app, name="add")
app.add_typer(default_completion_app, name="default-completion")

config_manager = ConfigManager()

def model_command(model: str):
    @api_keys_app.command(name=model)
    def add_model_config(
        api_key: Annotated[Optional[str], typer.Option("--api-key", help="API key for the model.")],
        base_url: Annotated[Optional[str], typer.Option("--base-url", help="Base URL for the API.")],
        api_type: Annotated[Optional[str], typer.Option("--api-type", help="Type of the API.")],
        api_version: Annotated[Optional[str], typer.Option("--api-version", help="API version.")],
        engine: Annotated[Optional[str], typer.Option("--engine", help="Engine for the API.")]
    ):
        # 当 api_type 为 azure 时，api_version 和 engine 是必须的
        if api_type == 'azure' and not all([api_version, engine]):
            raise typer.Exit("当 api_type 为 azure 时，必须提供 api_version 和 engine。")

        # 更新配置
        api_key_info = {
            'api_key': api_key,
            'base_url': base_url,
            'api_type': api_type,
            'api_version': api_version,
            'engine': engine
        }
        config_manager.update_partial_config('api_keys', {model: [api_key_info]})
        config_manager.save_config()
        typer.echo(f"模型 {model} 的 API key 配置已添加。")

models = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k"]
for model in models:
    model_command(model)

@default_completion_app.command()
def set_default_completion_kwargs(
    model: Annotated[Optional[str], typer.Option("--model", help="Default model for completions.", show_default=False)] = 'gpt-3.5-turbo',
    temperature: Annotated[Optional[float], typer.Option("--temperature", help="Default temperature for completions.")] = 0.2,
    request_timeout: Annotated[Optional[int], typer.Option("--request-timeout", help="Default request timeout in seconds.")] = 60
):
    # Update values from CLI or use existing ones from the config file
    updated_values = {
        'model': model,
        'temperature': temperature ,
        'request_timeout': request_timeout,
    }

    # Update the config dictionary
    config_manager.update_partial_config('default_completion_kwargs', updated_values)
    typer.echo("Default completion configurations updated.")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
    repo_path: Annotated[str, typer.Option(help="Path to the repository.", show_default=False)] = None,
    project_hierarchy: Annotated[Optional[str], typer.Option("--project-hierarchy", "-ph", help="Project hierarchy configuration file.")] = '.project_hierarchy.json',
    markdown_docs_folder: Annotated[Optional[str], typer.Option("--markdown-docs-folder", "-mdf", help="Folder for Markdown documentation.")] = 'Markdown_Docs',
    ignore_list: Annotated[Optional[List[str]], typer.Option("--ignore-list", "-il", help="List of files or directories to ignore.")] = None,
    language: Annotated[Optional[str], typer.Option("--language", "-l", help="Language option for the CLI.")] = 'zh'
):
    if ctx.invoked_subcommand is None:
        if not repo_path:
            raise typer.Exit("错误：必须提供目标仓库路径（repo_path）。")
    
        # 如果命令行参数未提供（即为 None），则从配置文件获取值，如果配置文件也没有，则保留 None 或设置默认值
        config_manager.update_partial_config('repo_path', repo_path)
        config_manager.update_partial_config('project_hierarchy', project_hierarchy)
        config_manager.update_partial_config('markdown_docs_folder', markdown_docs_folder)
        if ignore_list is not None:
            config_manager.update_partial_config('ignore_list', ignore_list)
        config_manager.update_partial_config('language', language)
        typer.echo("基础配置已更新。")


if __name__ == "__main__":
    app()
