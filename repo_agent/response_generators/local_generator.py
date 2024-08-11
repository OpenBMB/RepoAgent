from repo_agent.response_generators.response import Response
from repo_agent.response_generators.response_generator import ResponseGenerator


class LocalGenerator(ResponseGenerator):
    pipe = None

    def generate(self, model: str, sys_prompt: str, usr_prompt: str,
                 max_tokens: int) -> Response:
        from transformers import pipeline
        import torch
        hf_token = self.settings.chat_completion.huggingface_api_key.get_secret_value()
        messages = self._get_messages(sys_prompt, usr_prompt)
        cls = type(self)
        cls.pipe = cls.pipe or _PipelineWrapper(
            pipeline(
                "text-generation",
                model=model,
                model_kwargs={"torch_dtype": torch.bfloat16},
                device="cuda",
                token=hf_token
            ),
            max_tokens,
        )
        outputs = cls.pipe(messages, max_new_tokens=max_tokens)
        return Response(outputs[0]["generated_text"][-1]["content"].strip())

    def is_valid(self, model: str) -> bool:
        headers = {
            'Authorization': f'Bearer {self.settings.chat_completion.huggingface_api_key.get_secret_value()}'
        }
        return requests.get(f'https://api.huggingface.co/models/{model}',
                     headers=headers).status_code == 200

    def _get_messages(self, sys_prompt: str, usr_prompt: str) -> list[
        dict[str, str]]:
        return [
            {"role": "user", "content": f"{sys_prompt}\n{usr_prompt}"},
        ]


class _PipelineWrapper:
    def __init__(self, pipeline, max_new_tokens: int):
        self.max_new_tokens = max_new_tokens
        self.pipeline = pipeline

    def invoke(self, messages) -> Response:
        return Response(
            self.pipeline(messages, max_new_tokens=self.max_new_tokens)[
                0
            ]["generated_text"][-1]["content"].strip()
        )
