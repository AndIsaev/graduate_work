from .schema_template import TEMPLATE_INDEX_BODY

PERSON_INDEX_BODY: dict = {
    **TEMPLATE_INDEX_BODY,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "full_name": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {"raw": {"type": "keyword"}},
            },
            "roles": {"type": "keyword", "analyzer": "ru_en"},
            "film_ids": {"type": "keyword", "analyzer": "ru_en"},
        },
    },
}
