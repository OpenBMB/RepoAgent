import pytest
from repo_agent.config_manager import read_config, write_config, update_config_section
from tomlkit.toml_document import TOMLDocument

# 示例 TOML 文件内容
SAMPLE_TOML_CONTENT = """
[example]
key = "value"
"""


def test_read_config_success(tmp_path):
    # 创建一个临时的 TOML 文件
    temp_file = tmp_path / "temp_config.toml"
    temp_file.write_text(SAMPLE_TOML_CONTENT)

    # 测试读取
    config = read_config(str(temp_file))
    assert isinstance(config, TOMLDocument)
    assert config["example"]["key"] == "value"


def test_read_config_file_not_found():
    with pytest.raises(SystemExit):
        read_config("non_existent_file.toml")


def test_write_config_success(tmp_path):
    # 创建一个临时的 TOML 文件
    temp_file = tmp_path / "temp_config.toml"
    temp_file.write_text(SAMPLE_TOML_CONTENT)

    # 测试写入
    new_config = {"example": {"key": "new_value"}}
    write_config(new_config, str(temp_file))

    # 验证更新
    updated_config = read_config(str(temp_file))
    assert updated_config["example"]["key"] == "new_value"


def test_write_config_file_error():
    with pytest.raises(SystemExit):
        write_config({}, "non_existent_file.toml")


def test_update_config_section():
    config = {}
    updates = {"new_key": "new_value"}
    update_config_section(config, "new_section", updates)

    assert "new_section" in config
    assert config["new_section"]["new_key"] == "new_value"
