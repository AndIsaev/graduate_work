import aioredis
import uvicorn
from api.v1 import film, genre, person
from core import config
from db import cache, elastic, redis, storage
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=config.PROJECT_NAME,  # Конфигурируем название проекта
    description=config.PROJECT_NAME,
    version=config.VERSION,  # Указываем версию проекта
    docs_url="/api/openapi",  # Адрес документации в красивом интерфейсе
    openapi_url="/api/openapi.json",  # Адрес документации в формате OpenAPI
    redoc_url="/api/redoc",  # Альтернативная документация
    default_response_class=ORJSONResponse,
    # Можно сразу сделать небольшую оптимизацию сервиса и заменить
    # стандартный JSON-сереализатор на более шуструю версию, написанную на Rust
)


@app.get("/")
async def root():
    return {"service": config.PROJECT_NAME, "version": config.VERSION}


@app.on_event("startup")
async def startup():
    """Подключаемся к базам при старте сервера"""

    cache.cache = redis.CacheRedis(
        cache_instance=await aioredis.create_redis_pool(
            (config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20
        )
    )
    storage.storage = elastic.StorageElasticsearch(
        storage_instance=AsyncElasticsearch(
            hosts=[f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"]
        )
    )


@app.on_event("shutdown")
async def shutdown():
    """Отключаемся от баз при выключении сервера"""
    await cache.cache.close()
    await storage.storage.close()


# Подключаем роутеры к серверу
app.include_router(router=film.router, prefix="/api/v1/film")
app.include_router(router=genre.router, prefix="/api/v1/genre")
app.include_router(router=person.router, prefix="/api/v1/person")


if __name__ == "__main__":
    uvicorn.run("main:elastic", host="0.0.0.0", port=8000)
