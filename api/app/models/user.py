from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(
        String(50, collation="C"),
        index=True,
        unique=True,
        nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(50))
    is_blacklisted: Mapped[bool] = mapped_column(default=False)