from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User

async def get_user(session: AsyncSession, tg_id: str) -> User:
    statement = select(User).where(User.tg_id == tg_id)
    
    result = await session.scalar(statement)

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return result