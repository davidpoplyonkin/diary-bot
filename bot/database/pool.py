import asyncpg

from globals import (POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD,
                     POSTGRES_USER)

pool = None

async def get_pool():
    """
    Initialize a connection pool.
    """

    global pool

    if pool is None:
        pool = await asyncpg.create_pool(
            database=POSTGRES_DB,
            host=POSTGRES_HOST,
            password=POSTGRES_PASSWORD,
            user=POSTGRES_USER,
        )
    
    return pool
