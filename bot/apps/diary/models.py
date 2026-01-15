from database.pool import get_pool

class HealthMetric():
    async def create_table():
        """
        Create the `health_metrics` table if it doesn't exist.
        """

        pool = await get_pool()
        
        async with pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS health_metrics (
                    id SERIAL PRIMARY KEY,
                    metric VARCHAR(50) NOT NULL,
                    user_tg_id BIGINT NOT NULL REFERENCES users(tg_id),
                    value REAL NOT NULL,
                    date DATE NOT NULL
                );
            """)

    async def insert_many(
            user_tg_id: int,
            date: str,
            metrics: list, # [(m1, v1), (m2, v2), ...]
        ):
        """
        Add the user's health metric value to the database
        """

        pool = await get_pool()

        q_vals = [f"($1, $2, ${i}, ${i + 1})" for i in range(3, len(metrics)*2 + 3, 2)]
        q_args = [user_tg_id, date] + [i for t in metrics for i in t]
        q = f"""
            INSERT INTO health_metrics (user_tg_id, date, metric, value)
            VALUES {', '.join(q_vals)};
        """

        async with pool.acquire() as conn:
            await conn.execute(q, *q_args)

    async def get_many(**kwargs):
        """
        Return the rows that meet the specified constraints on user_tg_id,
        date, metric, value.
        """

        pool = await get_pool()

        args = []
        conditions = []

        for j, i in enumerate(kwargs.items(), start=1):
            k, v = i
            args.append(v)
            conditions.append(f"{k} = ${j}")

        async with pool.acquire() as conn:
            return await conn.fetch(f"""
                SELECT *
                FROM health_metrics
                WHERE {' AND '.join(conditions)};
            """, *args)
        
    async def get_recent(
            user_tg_id: int,
            metric: str,
            date: str,
            window: int,
        ):
        """
        Return the records newer than `date` - `window`.
        """

        pool = await get_pool()

        async with pool.acquire() as conn:
            return await conn.fetch("""
                SELECT *
                FROM health_metrics
                WHERE user_tg_id = $1
                    AND metric = $2
                    AND date > $3::date - (CAST($4 AS INT) * INTERVAL '1 day')
                    AND date <= $3::date;
            """, user_tg_id, metric, date, window)