from datetime import datetime
from typing import Any, Generator, Optional, Union

from config import EsIndex
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from query import GENRE_QUERY, MOVIE_QUERY, PERSON_QUERY
from state import JsonFileStorage, State


class PostgresLoader:
    def __init__(self, pg_conn: _connection) -> None:
        self.conn = pg_conn
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.key: Optional[str] = None
        self.batch = 100
        self.data: list = []
        self.count = 0

    def get_state_key(self) -> Union[datetime, Any]:
        """
        Определяем какую дату будем использовать для сравнения при запросе.
        """
        time = State(JsonFileStorage(file_path="postgres_data.txt")).get_state(self.key)
        if time is None:
            return datetime(2005, 7, 14, 12, 30)

        return time

    def loader_from_postgresql(self) -> Generator:
        """
        Главный запрос на получение данных из бд.
        """
        sql_requests = {
            EsIndex.MOVIES_INDEX: MOVIE_QUERY,
            EsIndex.GENRE_INDEX: GENRE_QUERY,
            EsIndex.PERSON_INDEX: PERSON_QUERY,
        }

        for key in sql_requests:
            self.key = key
            self.cursor.execute(sql_requests[key] % self.get_state_key())
            yield {"index": key, "result": self.cursor.fetchall()}
