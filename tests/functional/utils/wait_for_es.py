import logging
import os
from datetime import datetime
from time import sleep

import requests
from dotenv import load_dotenv

load_dotenv()


def wait_for_es(
    url: str = f"http://{os.getenv('ELASTIC_HOST')}:{os.getenv('ELASTIC_PORT')}",
):
    """Дождаться пока по адресу url заработает сервер ElasticSearch"""
    # Отправляем запрос в Elastic
    start_sleep_time: float = 0.1
    border_sleep_time: int = 3
    count: int = 0
    while count < 10:
        response = requests.get(url=url)
        if response.json().get("tagline", "").lower() == "you know, for search":
            return
        else:
            # Ответ Elastic не корректный, попробуем позже
            sleep(start_sleep_time)
            if start_sleep_time >= border_sleep_time:
                start_sleep_time = border_sleep_time
            elif start_sleep_time < border_sleep_time:
                start_sleep_time *= 2
            count += 1
            continue
    logging.error(f"{datetime.now()}\n" f"Исчерпано макс. кол-во подключений={count}.")


wait_for_es()
