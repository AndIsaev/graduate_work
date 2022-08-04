import logging
import time
from datetime import datetime

import psycopg2
from config import AWAIT_SECONDS, COLUMNS, ES_SCHEMAS, dsn, es_conf
from elasticsearch_loader import ElasticSearchLoader
from postgres_loader import PostgresLoader
from services import backoff

logger = logging.getLogger("LoaderStart")


@backoff()
def save_data_to_elastic() -> None:
    """
    Загружаем пачками данные в ElasticSearch, предварительно создаем индекс в бд.
    """
    elastic = ElasticSearchLoader(es_conf)

    logger.info(f"{datetime.now()}\n\nустановлена связь с ElasticSearch.")

    with psycopg2.connect(**dsn) as conn:
        logger.info(
            f"{datetime.now()}\n\nустановлена связь с PostgreSQL. Начинаем загрузку данных"
        )

        postgres_loader = PostgresLoader(pg_conn=conn)
        for data in postgres_loader.loader_from_postgresql():
            key = data["index"]

            elastic.create_index(index_name=key, index_body=ES_SCHEMAS[key])

            logger.info(
                f"{datetime.now()}\n\nНачинаем загрузку данных в ElasticSearch, индекс: {key}"
            )

            batch = 50
            count = len(data["result"])
            index = 0
            transformed_data = []

            while count != 0:
                if count >= batch:
                    for row in data["result"][index: index + batch]:
                        transformed_data.append(dict(zip(COLUMNS[key], row)))
                        index += 1
                    count -= batch
                    elastic.load_data_to_elasticsearch(
                        data_from_postgres=transformed_data, index_name=key
                    )
                    transformed_data.clear()
                else:
                    elastic.load_data_to_elasticsearch(
                        data_from_postgres=[
                            dict(zip(COLUMNS[key], row))
                            for row in data["result"][index: index + count]
                        ],
                        index_name=key,
                    )
                    count -= count


if __name__ == "__main__":
    while True:
        logger.info(f"Начинаем ETL процесс. Ждем {AWAIT_SECONDS} секунд.")
        save_data_to_elastic()
        logger.info(f"End ETL state process. Ждем {AWAIT_SECONDS} секунд.")
        time.sleep(AWAIT_SECONDS)
