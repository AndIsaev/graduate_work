import os

import psycopg2
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from psycopg2.extensions import connection as _connection


def load_data(ps_2: _connection) -> None:
    tables = ("film_work", "genre", "person", "genre_film_work", "person_film_work")
    psycopg2_cursor = ps_2.cursor()

    for table in tables:
        psycopg2_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        results = psycopg2_cursor.fetchone()[0]

        if results == 0:
            """Sending got data to postgresql db."""
            with open(f"movies/management/test_data/dump_{table}.csv", "r") as data:
                next(data)
                psycopg2_cursor.copy_expert(f"COPY {table} FROM STDIN with csv", data)
        else:
            print("Данные уже заполнены")


def create_superuser():
    users = User.objects.count()
    if users == 0:
        User.objects.create_superuser(
            username=os.getenv("DJANGO_SUPERUSER_USERNAME"),
            password=os.getenv("DJANGO_SUPERUSER_PASSWORD"),
            email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
        )
    else:
        print("админ уже создан")


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
            create_superuser()
