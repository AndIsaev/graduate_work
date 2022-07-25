from typing import Dict


class Request:
    def __init__(self, request_body: Dict):
        self.request_body = request_body

    def __getitem__(self, key: str) -> Dict:
        return self.request_body.get(key, {})

    @property
    def intents(self) -> Dict:
        return self.request_body.get("request", {}).get("nlu", {}).get("intents", {})

    @property
    def type(self) -> str:
        return self.request_body.get("request", {}).get("type")
