# repo_agent/log.py
import sys
import logging
from loguru import logger
from repo_agent.config import CONFIG

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
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Log to Loguru
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def set_logger_level_from_config():
    log_level = CONFIG.get("log_level", "INFO").upper()

    try:
        logger.remove()
        logger.add(sys.stderr, level=log_level)

        # Intercept standard logging
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        logger.success(f"Log level set to {log_level}!")
    except ValueError:
        logger.warning(
            f"Invalid log level '{log_level}' in config. Using default log level."
        )


# Automatically set logger level from config when module is imported
set_logger_level_from_config()


# TODO 由 Loguru 接管 Print
# 重定向标准输出和错误输出, :
# - `stdout` 被重定向至 logger 的 INFO 等级。
# - `stderr` 被重定向至 logger 的 ERROR 等级。
# class StreamToLogger:
#     """
#     Fake file-like stream object that redirects writes to a logger instance.

#     Args:
#         logger (loguru.Logger): The logger instance to which the output will be redirected.
#         level (str, optional): Log level for the messages. Defaults to 'INFO'.

#     Methods:
#         write(buffer): Redirects the buffer to the logger.
#         flush(): Dummy method to comply with file-like interface.
#     """

#     def __init__(self, logger, level="INFO"):
#         self.logger = logger
#         self._level = level

#     def write(self, buffer):
#         for line in buffer.rstrip().splitlines():
#             self.logger.opt(depth=1).log(self._level, line.rstrip())

#     def flush(self):
#         pass


# # Redirect stdout to logger at success level
# sys.stdout = StreamToLogger(logger)

# Redirect stderr to logger at error level
# sys.stderr = StreamToLogger(logger, "ERROR")

# import stackprinter


# def handle_exception(exc_type, exc_value, exc_traceback):
#     """
#     Custom exception handler using stackprinter for formatting.

#     Args:
#         exc_type: Exception type.
#         exc_value: Exception value.
#         exc_traceback: Exception traceback.
#     """
#     # Use stackprinter to format the exception and traceback
#     formatted_exception = stackprinter.format(exc_value, exc_traceback, style='plaintext')

#     # Log the formatted exception
#     logger.error("Unhandled exception:\n{}", formatted_exception)

# # Set the custom exception handler
# sys.excepthook = handle_exception
