import os

from api.models import Person
from api.search import SearchConnector


def get_search_es_connection():
    es_api_url = os.environ.get("ES_API_URL")
    return SearchConnector(es_api_url)


def decapitalize(text: str):
    """Upper first letter of text."""
    text = text.strip()
    return text[:1].upper() + text[1:]


def get_person_names(persons: list[Person]):
    return [person.full_name for person in persons if person]
