import abc
import json
import logging
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict[Any, Any]:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        if self.file_path is None:
            return

        with open(self.file_path, "w") as f:
            json.dump(state, f)

    def retrieve_state(self) -> Any:
        if self.file_path is None:
            logging.info("Не установлен путь до файла.")
            return {}

        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                if not data:
                    return {}

            return data

        except FileNotFoundError:
            self.save_state({})


class State:
    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage
        self.state = self.retrieve_state()

    def retrieve_state(self) -> dict:
        data = self.storage.retrieve_state()
        if not data:
            return {}
        return data

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.state[key] = value

        self.storage.save_state(self.state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        return self.state.get(key)
