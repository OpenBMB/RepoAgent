# repo_agent/log.py
import inspect
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
    logger.debug(f"Debugging info: {some_debug_variable}")

    # 记录警告信息
    logger.warning("This is a warning message")

    # 记录错误信息
    logger.error("An error occurred")
    ```

"""


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def set_logger_level_from_config(log_level):
    """
    Configures the loguru logger with specified log level and integrates it with the standard logging module.

    Args:
        log_level (str): The log level to set for loguru (e.g., "DEBUG", "INFO", "WARNING").

    This function:
    - Removes any existing loguru handlers to ensure a clean slate.
    - Adds a new handler to loguru, directing output to stderr with the specified level.
      - `enqueue=True` ensures thread-safe logging by using a queue, helpful in multi-threaded contexts.
      - `backtrace=False` minimizes detailed traceback to prevent overly verbose output.
      - `diagnose=False` suppresses additional loguru diagnostic information for more concise logs.
    - Redirects the standard logging output to loguru using the InterceptHandler, allowing loguru to handle
      all logs consistently across the application.
    """
    logger.remove()
    logger.add(
        sys.stderr, level=log_level, enqueue=True, backtrace=False, diagnose=False
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.success(f"Log level set to {log_level}!")
