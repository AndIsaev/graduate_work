from request import Request


class AliceRequest(Request):
    @property
    def intents(self) -> dict:
        return self.request_body.get("request", {}).get("nlu", {}).get("intents", {})

    @property
    def type(self) -> str:
        return self.request_body.get("request", {}).get("type")
