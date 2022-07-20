import asyncio
import logging
import os
from datetime import datetime

import aioredis
from dotenv import load_dotenv

load_dotenv()


async def wait_for_redis():
    start_sleep_time: float = 0.1
    border_sleep_time: int = 3
    count: int = 0
    redis_client = await aioredis.create_redis_pool(
        (os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT")), minsize=10, maxsize=20
    )
    while True:
        try:
            if await redis_client.ping():
                logging.info(f"{datetime.now()}\nSuccessfully connected to redis")
                break
        except Exception as e:
            await asyncio.sleep(start_sleep_time)
            if start_sleep_time >= border_sleep_time:
                start_sleep_time = border_sleep_time
            elif start_sleep_time < border_sleep_time:
                start_sleep_time *= 2
            logging.error(f"{datetime.now()}\n{e}\nПопытка подключение №{count}\n")
            count += 1
            continue
        finally:
            redis_client.close()
            await redis_client.wait_closed()
            if count == 10:
                logging.info(
                    f"{datetime.now()}\n\n"
                    f"Исчерпано максимальное количество подключений={count}\n"
                )
                break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_for_redis())
    loop.close()
