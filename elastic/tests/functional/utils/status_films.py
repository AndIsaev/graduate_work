from http import HTTPStatus
from typing import Optional


def check_films_result(
    status: int,
    expected_status: int,
    body: dict,
    expected_query: Optional[str],
    expected_page: Optional[str],
    expected_page_size: Optional[str],
) -> None:
    """
    Сверяем ожидаемые значения с результатом запросов.
    """
    # сравниваем с статус ответа с ожидаемым
    assert expected_status == status
    # находим вхождение ожидаемого query в результате
    # заведомо исключаем запрос с неправильной сортировкой чтобы найти вхождение
    if expected_query == "Star" and expected_status != HTTPStatus.NOT_FOUND:
        result_response = [res.get("title") for res in body.get("films")]
        for row in result_response:
            assert expected_query in row
    # проверяем что открыта правильная страница
    if expected_page:
        assert expected_page == body.get("page")
    # проверяем что фильмы приходят в запрошенном количестве
    if expected_page_size:
        assert expected_page_size == body.get("page_size")
