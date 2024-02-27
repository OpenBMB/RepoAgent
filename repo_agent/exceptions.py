from openai import APIConnectionError
from repo_agent.log import logger
class ErrorHandler:
    @staticmethod
    def handle_exception(e):
        if isinstance(e, APIConnectionError):
            logger.warning(f"OpenAIResponseError occurred: {e}")
            # Add your handling code here
        elif isinstance(e, OpenAIError):
            print(f"OpenAIError occurred: {e}")
            # Add your handling code here
        else:
            print(f"An unexpected error occurred: {e}")
            # Add your handling code here

class OpenAIError(Exception):
    def __init__(self, message):
        super().__init__(message)