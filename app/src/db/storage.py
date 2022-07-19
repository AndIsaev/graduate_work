from abc import ABC, abstractmethod
from typing import Optional


class AbstractStorage(ABC):
    def __init__(self, storage_instance):
        self.storage = storage_instance

    @abstractmethod
    def get(self, index: str, target_id: str):
        pass

    @abstractmethod
    def search(self, index: str, _source, body, sort):
        pass

    @abstractmethod
    def close(self):
        pass


storage: Optional[AbstractStorage] = None


# Функция понадобится при внедрении зависимостей
async def get_storage() -> AbstractStorage:
    return storage
