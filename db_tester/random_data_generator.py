from random import getrandbits
import asyncio
from faker import Faker

fake = Faker()


async def generate_random_data_async(rows: int = 10_000_000, batch_size: int = 1000) -> list[dict]:
    for _ in range(int(rows/batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {
                    "id": getrandbits(33),
                    "user_id": getrandbits(33),
                    "film_id": getrandbits(33),
                    "timestamp": str(fake.date_time_between())
                }
            )
        yield random_batch

def generate_random_data(rows: int = 10_000_000, batch_size: int = 1000) -> list[dict]:
    for _ in range(int(rows/batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {
                    "id": getrandbits(33),
                    "user_id": getrandbits(33),
                    "film_id": getrandbits(33),
                    "timestamp": str(fake.date_time_between())
                }
            )
        yield random_batch

# -- пример использования асихронного генератора
# async def get_data():
#     async for elem in generate_random_data_async():
#         print("Generated: %s" % elem[0])

# loop = asyncio.get_event_loop()
# loop.run_until_complete(get_data())
# loop.close()
