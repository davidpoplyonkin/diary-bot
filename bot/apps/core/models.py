from database.pool import get_pool

class User():
    async def create_table():
        """
        Crete the `users` table if it doesn't exist.
        """

        pool = await get_pool()
        
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    tg_id BIGINT UNIQUE NOT NULL,
                    full_name VARCHAR(50),
                    is_blacklisted BOOLEAN DEFAULT FALSE
                );
            """)

    async def upsert_one(tg_id: int, full_name: str):
        """
        If the user doesn't yet exist, add them to the database.
        Otherwise, update their name.
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (tg_id, full_name)
                VALUES ($1, $2)
                ON CONFLICT (tg_id)
                DO UPDATE SET full_name = EXCLUDED.full_name
            """, tg_id, full_name)

    async def get_one(tg_id: int):
        """
        Return the user with the specified ID.
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow("""
                SELECT *
                FROM users
                WHERE tg_id = $1;
            """, tg_id)

    async def blacklist(tg_id: int):
        """
        Add the specified user to the black list.
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            await conn.execute("""
                UPDATE users
                SET is_blacklisted = TRUE
                WHERE tg_id = $1
            """, tg_id)