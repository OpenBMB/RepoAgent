from typing import Optional

from transformers import pipeline
import torch
from repo_agent.response_generators.response import Response
from repo_agent.response_generators.response_generator import ResponseGenerator


class GemmaGenerator(ResponseGenerator):
    def generate(self, model: str, sys_prompt: str, usr_prompt: str,
                 max_tokens: int) -> Response:
        hf_token = self.setting.chat_completion.api_key.get_secret_value()
        pipe = pipeline(
            "text-generation",
            model=model,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device="cuda",
            token=hf_token,
        )
        messages = self._get_messages(sys_prompt, usr_prompt)
        outputs = pipe(messages, max_new_tokens=max_tokens)
        return Response(outputs[0]["generated_text"][-1]["content"].strip())

    @classmethod
    def is_valid(cls, model: str) -> bool:
        return not model.startswith("google/gemma")
