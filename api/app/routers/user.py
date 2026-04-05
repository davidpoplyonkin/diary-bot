from fastapi import APIRouter, Depends

from ..deps import DBSessionDep, admin_only
from ..crud import get_user, get_metrics
from ..schemas import UserMetrics

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/{user_tg_id}/metrics/{metric}",
    response_model=UserMetrics,
    dependencies=[Depends(admin_only)],
)
async def get_user_metrics(
    user_tg_id: str,
    metric: str,
    session: DBSessionDep,
):
    user = await get_user(session, user_tg_id)
    metrics = await get_metrics(session, user_tg_id, metric)

    return UserMetrics(user=user, metrics=metrics)
