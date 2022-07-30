import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from es_index import FILM_WORK_INDEX_BODY, GENRE_INDEX_BODY, PERSON_INDEX_BODY

dotenv_path = os.path.join(Path(__file__).resolve(strict=True).parent.parent, ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

logger = logging.getLogger()
logger.setLevel(level="INFO")

dsn = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}

es_conf = [
    {
        "host": os.getenv("ELASTIC_HOST"),
        "port": os.getenv("ELASTIC_PORT"),
    }
]

AWAIT_SECONDS = 10


class EsIndex:
    PERSON_INDEX: str = "persons"
    GENRE_INDEX: str = "genres"
    MOVIES_INDEX: str = "movies"


ES_SCHEMAS = {
    EsIndex.MOVIES_INDEX: FILM_WORK_INDEX_BODY,
    EsIndex.GENRE_INDEX: GENRE_INDEX_BODY,
    EsIndex.PERSON_INDEX: PERSON_INDEX_BODY,
}

COLUMNS = {
    EsIndex.MOVIES_INDEX: (
        "id",
        "title",
        "description",
        "imdb_rating",
        "genre",
        "actors",
        "writers",
        "directors",
    ),
    EsIndex.GENRE_INDEX: (
        "id",
        "name",
    ),
    EsIndex.PERSON_INDEX: (
        "id",
        "full_name",
        "roles",
        "film_ids",
    ),
}
