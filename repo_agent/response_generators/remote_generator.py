from typing import Optional

from repo_agent.response_generators.response import Response
from repo_agent.response_generators.response_generator import ResponseGenerator
from openai import OpenAI

class RemoteGenerator(ResponseGenerator):
    def generate(self, model: str, sys_prompt: str, usr_prompt: str,
                 max_tokens: int) -> Optional[Response]:
        messages = self._get_messages(sys_prompt, usr_prompt)
        llm = init_chat_model(model, temperature=0.2)
        response_message = llm.invoke(messages)
        if isinstance(response_message, Response):
            return response_message
        return
    
    @classmethod
    def is_valid(cls, model: str) -> bool:
        try:
            return bool(init_chat_model(config.llm, temperature=0.2))
        except ValueError | ValidationError:
            return False

    def _get_messages(self, sys_prompt: str, usr_prompt: str) -> list[dict[str, str]]:
        return [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": usr_prompt},
        ]
        