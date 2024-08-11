from repo_agent.response_generators.response_generator import ResponseGenerator
from repo_agent.settings import Setting


class ResponseGeneratorFactory:
    @classmethod
    def create(cls, settings: Setting, model: str) -> ResponseGenerator:
        for class_ in ResponseGenerator.__subclasses__():
            if class_(settings).is_valid(model):
                return instance
        raise ValueError(f"{model=} is not valid")


