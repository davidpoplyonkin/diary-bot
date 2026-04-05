from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..models import HealthMetric

async def get_metrics(
        session: AsyncSession,
        user_tg_id: str,
        metric: str
    ) -> List[HealthMetric]:

    statement = select(HealthMetric).where(
        HealthMetric.user_tg_id == user_tg_id,
        HealthMetric.metric == metric
    ).order_by(HealthMetric.id.desc())

    results = await session.execute(statement)
    
    return results.scalars().all()
