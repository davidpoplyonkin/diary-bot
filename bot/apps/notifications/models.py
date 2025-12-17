from database.pool import get_pool

class Notification():
    async def create_table():
        """
        Create the `notifications` table if it doesn't exist.
        """

        pool = await get_pool()
        
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id SERIAL PRIMARY KEY,
                    metric VARCHAR(50) NOT NULL,
                    user_tg_id BIGINT NOT NULL REFERENCES users(tg_id),
                    time TIME NOT NULL
                );
            """)

    async def insert_one(user_tg_id: int, metric: str, time: str):
        """
        Insert the notification.
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO notifications (user_tg_id, metric, time)
                VALUES ($1, $2, $3)
            """, user_tg_id, metric, time)

    async def get_many(user_tg_id: int):
        """
        Return the scheduled notifications for the specified user.
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetch(f"""
                SELECT * FROM notifications
                WHERE user_tg_id = $1
                ORDER BY time;
            """, user_tg_id)
        
    async def get_one(user_tg_id: int, metric: str):
        """
        Return the scheduled notifications for the specified user and
        metric.
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetchrow(f"""
                SELECT * FROM notifications
                WHERE user_tg_id = $1 AND metric = $2;
            """, user_tg_id, metric)
        
    async def delete_many(user_tg_id: int, metric: str):
        """
        Remove the specified notification.
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            await conn.execute(f"""
                DELETE FROM notifications
                WHERE user_tg_id = $1 AND metric = $2
            """, user_tg_id, metric)
