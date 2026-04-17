from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from ..models import User

async def get_user(session: AsyncSession, tg_id: str) -> User:
    statement = select(User).where(User.tg_id == tg_id)
    
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404)
    
    return user

async def upsert_user(
    session: AsyncSession,
    tg_id: str,
    full_name: str
) -> User:
    stmt = insert(User).values(tg_id=tg_id, full_name=full_name)

    statement = (
        stmt.on_conflict_do_update(
            index_elements=["tg_id"], # columns with the unique constraint
            set_={ # columns to update
                "full_name": stmt.excluded.full_name,
            }
        )
        .returning(User) # return the updated user
        .execution_options(populate_existing=True)
    )

    result = await session.execute(statement)
    user = result.scalar_one()

    await session.commit()
    return user

async def blacklist_user(session: AsyncSession, tg_id: str) -> User:
    statement = (
        update(User)
        .where(User.tg_id == tg_id)
        .values(is_blacklisted=True)
        .returning(User)
        .execution_options(populate_existing=True)
    )

    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404)

    await session.commit()
    return user
