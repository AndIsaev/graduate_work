import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    FASTAPI_HOST = os.getenv("FASTAPI_HOST")
    FASTAPI_PORT = os.getenv("FASTAPI_PORT")
    SERVICE_URL: str = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}"
    # ELASTIC
    ELASTIC_HOST: str = os.getenv("ELASTIC_HOST")
    ELASTIC_PORT: int = os.getenv("ELASTIC_PORT")
    ELASTIC_URL: str = f"{ELASTIC_HOST}:{ELASTIC_PORT}"
    # REDIS
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = os.getenv("REDIS_PORT")
    # ELASTIC Indexes
    PERSON_INDEX: str = "person_test"
    GENRE_INDEX: str = "genre_test"
    MOVIES_INDEX: str = "movies_test"
