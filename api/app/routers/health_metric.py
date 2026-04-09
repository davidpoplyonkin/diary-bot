from fastapi import APIRouter, Depends
import datetime

from ..deps import DBSessionDep, authorize_current_user
import app.crud as crud
from schemas import (UserMetricsSchema, Role, HealthMetricInputSchema,
                     HealthMetricOutputSchema)

router = APIRouter(
    prefix="/users/{user_tg_id}/metrics",
    tags=["metrics"],
    responses={404: {"description": "Metric not found"}},
)

@router.get(
    "/{metric}/{date}",
    response_model=HealthMetricOutputSchema,
    dependencies=[Depends(authorize_current_user([Role.ADMIN]))],
)
async def get_metric(
    user_tg_id: str,
    metric: str,
    date: datetime.date,
    session: DBSessionDep,
):
    metric = await crud.get_metric(session, user_tg_id, metric, date)

    return metric

@router.get(
    "/{metric}",
    response_model=UserMetricsSchema,
    dependencies=[Depends(authorize_current_user([Role.ADMIN]))],
)
async def get_user_metrics(
    user_tg_id: str,
    metric: str,
    session: DBSessionDep,
):
    user = await crud.get_user(session, user_tg_id)
    metrics = await crud.get_metrics(session, user_tg_id, metric)

    return UserMetricsSchema(user=user, metrics=metrics)

@router.post(
    "/bulk",
    dependencies=[Depends(authorize_current_user([Role.ADMIN]))],
)
async def bulk_insert_metrics(
    user_tg_id: str,
    metrics: list[HealthMetricInputSchema],
    session: DBSessionDep
) -> None:
    await crud.bulk_insert_metrics(session, user_tg_id, metrics)
