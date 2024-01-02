from dynaconf import Dynaconf, Validator, loaders, ValidationError
from dynaconf.utils.boxing import DynaBox


settings = Dynaconf(
    environments=True, 
    env="production", 
    settings_files="repo_agent/configs/settings.toml",    
    envvar_prefix="REPOAGENT"
)

settings.validators.register(
    Validator("OPENAI_API_KEY", must_exist=True),

    Validator(
        "chat_completion_kwargs.model",
        must_exist=True,
        condition=lambda value: case_insensitive_in(value, [
            "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-1106",
            "gpt-4", "gpt-4-32k", "gpt-4-1106-preview",
        ])
    ),

    # temperature 必须在 0 到 1 之间
    Validator("chat_completion_kwargs.temperature", must_exist=True, 
              is_type_of=float, gte=0, lte=1),

    # request_timeout 必须在 0 到 60 之间
    Validator("chat_completion_kwargs.request_timeout", must_exist=True, 
              is_type_of=int, gte=0, lte=60),

    # base_url 必须以 http 开头
    Validator("chat_completion_kwargs.base_url", must_exist=True, is_type_of=str,
              condition=lambda value: value.startswith("http")),
)

def export_settings():
    # 获取当前环境的配置
    data = settings.as_dict()
    
    # 将配置写入 SETTINGS_MODULE 指定的文件
    loaders.write(settings.SETTINGS_MODULE, DynaBox(data).to_dict(), merge=False, env=settings.current_env)

    # 重新加载配置以应用更新
    settings.reload()

def validate_settings() -> str | None:
    """
    验证 Dynaconf settings 中的所有配置。

    这个函数尝试使用 Dynaconf 的 validators 对象的 validate_all 方法
    来校验配置中的所有设置项。如果有任何验证错误，它会捕获 ValidationError
    并格式化错误信息。

    返回:
        str: 如果有验证错误，返回格式化的错误信息字符串；
             如果没有错误，返回 None。
    """
    try:
        settings.validators.validate_all()
    except ValidationError as e:
        # 格式化错误信息
        friendly_errors = [str(message) for _, message in e.details]
        return "\n".join(friendly_errors)
    return None

def case_insensitive_in(value: str, valid_values: list[str]) -> bool:
    """
    检查一个字符串值是否存在于一个字符串列表中，不区分大小写。

    参数:
        value (str): 需要检查的字符串值。
        valid_values (list of str): 一个包含有效字符串的列表。

    返回:
        bool: 如果 value（不区分大小写）存在于 valid_values 中，则返回 True；
              否则返回 False。
    """
    return value.lower() in [v.lower() for v in valid_values]
