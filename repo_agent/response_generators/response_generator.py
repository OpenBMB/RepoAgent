from abc import ABC, abstractmethod
from typing import Optional

from repo_agent.response_generators.response import Response
from repo_agent.settings import Setting


class ResponseGenerator(ABC):
    setting: Setting

    def __init__(self, settings: Setting):
        self.settings = settings

    @abstractmethod
    def generate(self, model: str, sys_prompt: str, usr_prompt: str,
                 max_tokens: int) -> Optional[Response]:
        pass

    @classmethod
    @abstractmethod
    def is_valid(cls, model: str) -> bool:
        pass

    def _get_messages(self, sys_prompt: str, usr_prompt: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": usr_prompt},
        ]
