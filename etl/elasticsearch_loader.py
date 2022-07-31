import json
import logging
from datetime import datetime

from elasticsearch import Elasticsearch
from services import backoff
from state import JsonFileStorage, State

logger = logging.getLogger("ESLoader")


class ElasticSearchLoader:
    def __init__(self, host: list):
        self.client = Elasticsearch(host)
        self.data: list = []
        self.key = "movies"

    @backoff()
    def create_index(self, index_name: str, index_body: dict) -> None:
        """
        Создаем индекс для Elasticsearch.
        """
        if not self.client.indices.exists(index=index_name):
            try:
                self.client.indices.create(index=index_name, body=index_body)
            except Exception as e:
                logger.warning(e)
            logger.warning(f"{datetime.now()}\n\nиндекс {index_name} создан")
        else:
            logger.warning(f"{datetime.now()}\n\nиндекс {index_name} был создан ранее")

    @backoff()
    def bulk_data_to_elasticsearch(self, index_name: str) -> None:
        self.client.bulk(index=index_name, body=self.data, refresh=True)

    def load_data_to_elasticsearch(self, data_from_postgres: list, index_name: str) -> None:
        """
        Загружаем данные пачками в Elasticsearch предварительно присваивая записям id.
        """
        self.key = index_name
        data_json = json.dumps(data_from_postgres)
        load_json = json.loads(data_json)

        for row in load_json:
            self.data.append({"create": {"_index": index_name, "_id": row["id"]}})
            self.data.append(row)
            self.bulk_data_to_elasticsearch(index_name=index_name)
            self.data.clear()
        State(JsonFileStorage("postgres_data.txt")).set_state(str(self.key), value=str(datetime.now()))
