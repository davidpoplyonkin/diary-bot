from pydantic import BaseModel, ConfigDict, Field
import datetime

class HealthMetric(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    metric: str = Field(max_length=50)
    user_tg_id: str = Field(max_length=50)
    value: float
    date: datetime.date
