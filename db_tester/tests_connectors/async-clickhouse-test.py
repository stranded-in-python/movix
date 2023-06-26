import sys
sys.path.append("..")

import asyncio
from aiochclient import ChClient
from aiohttp import ClientSession
from datetime import datetime as dt

from random_data_generator import generate_random_data_async

async def main():
    async with ClientSession() as s:
        client = ChClient(s)
        assert await client.is_alive()
        await client.execute(
            "CREATE DATABASE IF NOT EXISTS test_db ON CLUSTER company_cluster"
        )
        await client.execute("""
        CREATE TABLE IF NOT EXISTS test_db.regular_table ON CLUSTER company_cluster 
        (id Int64, user_id Int64, film_id Int64, timestamp DateTime64)
        Engine=MergeTree() ORDER BY id""")
        
        stamp = dt.now()
        async for batch in generate_random_data_async():
            await client.execute(
                "INSERT INTO test_db.regular_table (id, user_id, film_id, timestamp) VALUES",
                *[row.values() for row in batch]
            )
        
        print("Time elapsed %s" % str(dt.now()-stamp))

        await client.execute(
            "DROP DATABASE IF EXISTS test_db ON CLUSTER company_cluster"
        )
        await client.execute("""
        DROP TABLE IF EXISTS test_db.regular_table ON CLUSTER company_cluster
        """)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
#Time elapsed 0:03:36.244357
