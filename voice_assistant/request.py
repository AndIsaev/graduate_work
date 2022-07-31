from abc import ABC, abstractmethod


class Request(ABC):
    def __init__(self, request_body: dict):
        self.request_body = request_body

    def __getitem__(self, key: str) -> dict:
        return self.request_body.get(key, {})

    @property
    @abstractmethod
    def intents(self) -> dict:
        pass

    @property
    @abstractmethod
    def type(self) -> str:
        pass
