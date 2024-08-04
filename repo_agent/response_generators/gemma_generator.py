from transformers import pipeline
import torch
from repo_agent.response_generators.response import Response
from repo_agent.response_generators.response_generator import ResponseGenerator


class GemmaGenerator(ResponseGenerator):
    pipe = None

    def generate(self, model: str, sys_prompt: str, usr_prompt: str,
                 max_tokens: int) -> Response:
        hf_token = self.settings.chat_completion.huggingface_api_key.get_secret_value()
        messages = self._get_messages(sys_prompt, usr_prompt)
        cls = type(self)
        cls.pipe = cls.pipe or pipeline(
            "text-generation",
            model=model,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device="cuda",
            token=hf_token,
        )
        outputs = cls.pipe(messages, max_new_tokens=max_tokens)
        return Response(outputs[0]["generated_text"][-1]["content"].strip())

    @classmethod
    def is_valid(cls, model: str) -> bool:
        return model.startswith("google/gemma")

    def _get_messages(self, sys_prompt: str, usr_prompt: str) -> list[
        dict[str, str]]:
        return [
            {"role": "user", "content": f"{sys_prompt}\n{usr_prompt}"},
        ]
