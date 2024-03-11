from openai import APIConnectionError

from repo_agent.log import logger


class ErrorHandler:
    @staticmethod
    def handle_exception(e):
        if isinstance(e, APIConnectionError):
            logger.warning(f"OpenAIResponseError occurred: {e}")
        elif isinstance(e, OpenAIError):
            logger.error(f"OpenAIError occurred: {e}")
        else:
            logger.error(f"An unexpected error occurred: {e}")

class OpenAIError(Exception):
    def __init__(self, message):
        super().__init__(message)