from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, String, ForeignKey, Date, Float
import datetime

from ..database import Base

class HealthMetric(Base):
    __tablename__ = "health_metrics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    metric: Mapped[str] = mapped_column(
        String(50, collation="C"),
        nullable=False,
    )
    user_tg_id: Mapped[int] = mapped_column(
        String(50, collation="C"),
        ForeignKey("users.tg_id"),
        nullable=False,
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        # Index for filtering by `user_tg_id` and `metric` and sorting by `date`
        # (sorting by `id` results in the same order as `date` but is faster)
        Index("ix_tg_metric_date", "user_tg_id", "metric", "id"),
    )