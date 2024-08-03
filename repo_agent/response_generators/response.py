from typing import Protocol, runtime_checkable


@runtime_checkable
class Response(Protocol):
    content: str

    def __init__(self, content: str):
        self.content = content
