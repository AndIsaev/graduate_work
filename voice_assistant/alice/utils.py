import os

from api.search import SearchConnector


def get_search_es_connection():
    es_api_url = os.environ.get("ES_API_URL")
    return SearchConnector(es_api_url)


def decapitalize(text):
    text = text.strip()
    return text[:1].lower() + text[1:]