# repo_agent/config_manager.py
import os
from pathlib import Path
from typing import Dict

import tomli
import tomli_w


def get_config_path() -> Path:
    # 首先检查当前工作目录的父目录
    parent_directory = Path.cwd()
    local_config_path = parent_directory / 'config.toml'

    # 如果在程序目录找到了 config.toml，则直接返回这个路径
    if local_config_path.exists():
        return local_config_path

    # 如果在父目录没有找到 config.toml，按照原来的逻辑进行
    os_name = os.name
    if os_name == 'posix':
        # 对于 Unix 和 macOS，使用家目录
        home_config_path = Path.home() / '.repoagent'
    elif os_name == 'nt':
        # 对于 Windows，使用 APPDATA 目录
        home_config_path = Path(os.getenv('APPDATA')) / 'repoagent' # type: ignore
    else:
        # 如果操作系统检测失败，默认使用一个本地目录
        home_config_path = Path.cwd() / 'repoagent'
    
    # 确保配置目录存在
    home_config_path.mkdir(parents=True, exist_ok=True)
    config_path = home_config_path / 'config.toml'
    
    # 确保配置文件存在，如果不存在则创建一个空文件
    if not config_path.exists():
        config_path.touch()

    # 返回包含文件名的完整路径
    return config_path


def read_config(file_path: Path | None = None) -> Dict[str, any]: # type: ignore

    if file_path is None:
        file_path = get_config_path()

    with open(file_path, "rb") as f:
        try:
            toml_dict = tomli.load(f)
        except tomli.TOMLDecodeError:
            toml_dict = {}

    return toml_dict



def write_config(update_config: dict, file_path: Path | None = None) -> None:
    if file_path is None:
        file_path = get_config_path()

    # 先尝试读取现有配置，如果文件不存在则创建一个空的字典
    with open(file_path, "rb") as f:
        try:
            existing_config = tomli.load(f)
        except tomli.TOMLDecodeError:
            existing_config = {}

    # 更新配置：将新配置的键和值更新到现有配置字典中
    existing_config.update(update_config)

    # 将更新后的配置写回文件
    with open(file_path, "wb") as f:
        tomli_w.dump(existing_config, f)

if __name__ == '__main__':
    # Sample TOML data to be written to the configuration file
    sample_toml_data = """\
    val2 = 2
    val1 = 1

    [table]
    val3 = 4
    """
    # Convert the TOML string to a dictionary
    sample_config = tomli.loads(sample_toml_data)

    # Write the TOML configuration to a file
    write_config(sample_config)

    # Read the configuration back from the file
    read_back_config = read_config()

    # Print the configuration to verify the contents
    print(read_back_config)

    print(sample_config)