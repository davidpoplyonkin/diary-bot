from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import datetime

from ..models import HealthMetric
from schemas import HealthMetricInputSchema

async def get_metric(
        session: AsyncSession,
        user_tg_id: str,
        metric: str,
        date: datetime.date
    ) -> List[HealthMetric]:
    statement = (
        select(HealthMetric)
        .where(
            HealthMetric.user_tg_id == user_tg_id,
            HealthMetric.metric == metric,
            HealthMetric.date == date
        )
    )

    result = await session.execute(statement)
    metric = result.scalar_one_or_none()

    if metric is None:
        raise HTTPException(status_code=404)
    
    return metric

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

async def bulk_insert_metrics(
    session: AsyncSession,
    user_tg_id: str,
    metrics: List[HealthMetricInputSchema]
) -> None:
    values = [{
        "user_tg_id": user_tg_id,
        "metric": metric.metric,
        "value": metric.value,
        "date": metric.date
    } for metric in metrics]

    if not values:
        return
    
    statement = insert(HealthMetric)
    await session.execute(statement, values)

    await session.commit()
