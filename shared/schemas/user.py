from pydantic import BaseModel, ConfigDict, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .health_metric import HealthMetricOutputSchema

class UserOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_id: str = Field(max_length=50)
    full_name: str = Field(max_length=50)
    is_blacklisted: bool = False

class UserInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tg_id: str = Field(max_length=50)
    full_name: str = Field(max_length=50)

class UserMetricsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserOutputSchema
    metrics: list["HealthMetricOutputSchema"]

from .health_metric import HealthMetricOutputSchema
UserMetricsSchema.model_rebuild(
    _types_namespace={"HealthMetricOutputSchema": HealthMetricOutputSchema}
)
