import hashlib


def create_hash_key(index: str, params: str) -> str:
    """
    :param index: индекс в elasticsearch
    :param params: параметры запроса
    :return: хешированый ключ в md5
    """
    hash_key = hashlib.md5(params.encode()).hexdigest()
    return f"{index}:{hash_key}"
