from loguru import logger
from request import Request


class AliceRequest(Request):
    @property
    def intents(self) -> dict:
        _intents = self.request_body.get("request", {}).get("nlu", {}).get("intents", {})
        logger.debug(f"Intents: {_intents}")
        return _intents

    @property
    def type(self) -> str:
        return self.request_body.get("request", {}).get("type")
