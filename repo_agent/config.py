from dynaconf import Dynaconf, Validator, loaders
from dynaconf.utils.boxing import DynaBox


settings = Dynaconf(
    environments=True, 
    env="production", 
    settings_files="repo_agent/configs/settings.toml",    
    envvar_prefix="REPOAGENT"
)

settings.validators.register(
    Validator("OPENAI_API_KEY", must_exist=True),
)

def export_settings():
    # 获取当前环境的配置
    data = settings.as_dict(env=settings.current_env)
    
    # 将配置写入 SETTINGS_MODULE 指定的文件
    loaders.write(settings.SETTINGS_MODULE, DynaBox(data).to_dict(), merge=False, env=settings.current_env)

    # 重新加载配置以应用更新
    settings.reload()
    