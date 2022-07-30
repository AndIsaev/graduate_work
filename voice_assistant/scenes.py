from abc import ABC, abstractmethod
from typing import Any

from request import Request


class Scene(ABC):
    @classmethod
    def id(cls) -> str:
        """Получение уникального номера класса."""
        return cls.__name__

    @abstractmethod
    def reply(self, request: Request) -> dict:
        """Генерация ответа сцены."""
        raise NotImplementedError()

    @abstractmethod
    def _make_response(self, text: str, **kwargs: Any) -> dict:
        """Генерация ответа в необходимой для voice assistant структуре."""
        raise NotImplementedError()
