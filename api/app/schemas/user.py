from pydantic import BaseModel, ConfigDict, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .health_metric import HealthMetric

class UserId(BaseModel):
    tg_id: str

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tg_id: str = Field(max_length=50)
    full_name: str = Field(max_length=50)
    is_blacklisted: bool = False

class UserMetrics(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: User
    metrics: list["HealthMetric"]

from .health_metric import HealthMetric
UserMetrics.model_rebuild(_types_namespace={"HealthMetric": HealthMetric})
