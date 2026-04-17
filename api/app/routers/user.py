from fastapi import APIRouter, Depends

from ..deps import DBSessionDep, authorize_current_user
import app.crud as crud
from schemas import UserInputSchema, UserOutputSchema, Role

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)

@router.get(
    "/{user_tg_id}",
    response_model=UserOutputSchema,
    dependencies=[Depends(authorize_current_user([Role.ADMIN]))],
)
async def get_user(user_tg_id: str, session: DBSessionDep):
    return await crud.get_user(session, user_tg_id)

@router.post(
    "/{user_tg_id}/blacklist",
    response_model=UserOutputSchema,
    dependencies=[Depends(authorize_current_user([Role.ADMIN]))],
)
async def blacklist_user(user_tg_id: str, session: DBSessionDep):
    return await crud.blacklist_user(session, user_tg_id)

@router.put(
    "/{user_tg_id}",
    response_model=UserOutputSchema,
    dependencies=[Depends(authorize_current_user([Role.ADMIN]))],
)
async def upsert_user(user: UserInputSchema, session: DBSessionDep):
    return await crud.upsert_user(session, user.tg_id, user.full_name)
