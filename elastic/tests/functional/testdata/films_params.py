from http import HTTPStatus

film_search_params = [
    # параметры с query
    ("film", {"query": "Star"}, HTTPStatus.OK),
    # параметры с query и страницей
    ("film", {"query": "Star", "page": 2}, HTTPStatus.OK),
    # параметры с query и и страницей и количеством фильмов в ответе
    ("film", {"query": "Star", "page": 2, "page_size": 3}, HTTPStatus.OK),
    # проверяем сортировку по возрастанию без параметра query
    ("film", {"query": "Star", "sort": "imdb_rating"}, HTTPStatus.OK),
    # проверяем сортировку по убыванию без параметра query
    ("film", {"query": "Star", "sort": "-imdb_rating"}, HTTPStatus.OK),
    # сортировка по несуществующему полю
    ("film", {"query": "Star", "sort": "test"}, HTTPStatus.NOT_FOUND),
    # поиск фильма с лучшим рейтингом и в жанре Drama
    (
        "film",
        {
            "query": "Bright",
            "page": 1,
            "page_size": 10,
            "sort": "-imdb_rating",
            "genre": "Drama",
        },
        HTTPStatus.OK,
    ),
]

film_list_params = [
    # параметры без query
    ("film", {}, HTTPStatus.OK),
    # параметры со страницами
    ("film", {"page": 2, "page_size": 1}, HTTPStatus.OK),
    # проверяем сортировку по возрастанию без параметра query
    ("film", {"sort": "imdb_rating"}, HTTPStatus.OK),
    # проверяем сортировку по убыванию без параметра query
    ("film", {"sort": "-imdb_rating"}, HTTPStatus.OK),
    # сортировка по несуществующему полю
    ("film", {"sort": "test"}, HTTPStatus.NOT_FOUND),
    # фильтрация по жанру
    ("film", {"genre": "Drama"}, HTTPStatus.OK),
]
