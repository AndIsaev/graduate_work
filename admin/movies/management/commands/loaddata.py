import os

import psycopg2
from django.core.management import BaseCommand
from psycopg2.extensions import connection as _connection


def load_data(ps_2: _connection) -> None:
    tables = ("film_work", "genre", "person", "genre_film_work", "person_film_work")
    psycopg2_cursor = ps_2.cursor()

    for table in tables:
        """Sending got data to postgresql db."""
        with open(f"movies/management/test_data/dump_{table}.csv", "r") as data:
            next(data)
            psycopg2_cursor.copy_expert(f"COPY {table} FROM STDIN with csv", data)


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        dsn = {
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "host": os.getenv("POSTGRES_HOST"),
            "port": os.getenv("POSTGRES_PORT"),
        }
        with psycopg2.connect(**dsn) as conn:
            load_data(conn)
