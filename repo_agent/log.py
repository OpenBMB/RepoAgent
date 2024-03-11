# repo_agent/log.py
import logging
import sys

from loguru import logger

logger = logger.opt(colors=True)
"""
RepoAgent 日志记录器对象。

默认信息:
- 格式: `[%(asctime)s %(name)s] %(levelname)s: %(message)s`
- 等级: `INFO` ，根据 `CONFIG["log_level"]` 配置改变
- 输出: 输出至 stdout

用法示例:
    ```python
    from repo_agent.log import logger
    
    # 基本消息记录
    logger.info("It <green>works</>!") # 使用颜色

    # 记录异常信息
    try:
        1 / 0
    except ZeroDivisionError:
        # 使用 `logger.exception` 可以在记录异常消息时自动附加异常的堆栈跟踪信息。
        logger.exception("ZeroDivisionError occurred")

    # 记录调试信息
    logger.debug("Debugging info: {}", some_debug_variable)

    # 记录警告信息
    logger.warning("This is a warning message")

    # 记录错误信息
    logger.error("An error occurred")

    # 使用原生 print 函数（被重定向至 logger）
    print("This will be logged as an INFO level message")
    ```

"""


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the logged message originated
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__: # type: ignore
            frame = frame.f_back # type: ignore
            depth += 1

        # Log to Loguru
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def set_logger_level_from_config(log_level):

    logger.remove()
    logger.add(sys.stderr, level=log_level)

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.success(f"Log level set to {log_level}!")


