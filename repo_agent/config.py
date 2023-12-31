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

    Validator("chat_completion_kwargs.model", must_exist=True, is_in=(
        "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k", "gpt-4-turbo")),

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
    data = settings.as_dict(env=settings.current_env)
    
    # 将配置写入 SETTINGS_MODULE 指定的文件
    loaders.write(settings.SETTINGS_MODULE, DynaBox(data).to_dict(), merge=False, env=settings.current_env)

    # 重新加载配置以应用更新
    settings.reload()

def validate_settings():
    try:
        settings.validators.validate_all()
    except ValidationError as e:
        # 格式化错误信息
        friendly_errors = [str(message) for _, message in e.details]
        return "\n".join(friendly_errors)
    return None