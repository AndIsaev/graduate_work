import random

from api.models import Film, Person, Genre

FAKE_FILMS: list[str] = [
    "Зеленая миля",
    "Список Шиндлера",
    "Побег из Шоушенка",
    "Форрест Гамп",
    "Властелин колец: Возвращение короля",
    "Властелин колец: Две крепости",
    "Властелин колец: Братство кольца",
    "Один плюс один",
    "Криминальное чтиво",
    "Тайна Коко",
    "Интерстеллар",
]

FAKE_PERSONS: list[str] = [
    "Гэри Олдмен",
    "Джеймс Макэвой",
    "Хавьер Бардем",
    "Лиа Мишель",
    "Джастин Хартли",
    "Венсан Кассель",
    "Антонио Бандерас",
    "Рики Джервэйс",
    "Колин Ферт",
    "Кристоф Вальц",
    "Джуд Лоу",
]

fake_tv_shows: list[str] = [
    "Рик и Морти",
    "Гравити Фолз",
    "Во все тяжкие",
    "Клиника",
    "Игра престолов",
    "Доктор Хаус",
    "Шерлок",
    "Южный парк",
    "Футурама",
    "Пацаны",
    "Офис",
]


def get_fake_film():
    return random.choice(FAKE_FILMS)


def get_fake_film_list(count: int = 3):
    film_list = []
    fake_film_list = FAKE_FILMS.copy()
    for _ in range(count):
        film = random.choice(fake_film_list)
        fake_film_list.remove(film)
        film_list.append(film)
    return film_list


def get_fake_actors(count: int = 3):
    actors = []
    person_list = FAKE_PERSONS.copy()
    for _ in range(count):
        person = random.choice(person_list)
        person_list.remove(person)
        actors.append(Person(**{"uuid": "e42d300d-d671-4877-aa3f-d7fb1ced52ad", "full_name": person}))
    return actors


def get_fake_film_data(film_name: str):
    return Film(
        **{
            "uuid": "e42d330d-d671-4877-aa3f-d7fb1ced52ad",
            "title": film_name,
            "description": "Борьба добра против зла.",
            "imdb_rating": 7.9,
            "genre": [Genre(**{"uuid": "e52d330d-d671-4877-aa3f-d7fb1ced52ad", "name": "Экшен"}),
                      Genre(**{"uuid": "e62d330d-d671-4877-aa3f-d7fb1ced52ad", "name": "Фантастика"})],
        }
    )
