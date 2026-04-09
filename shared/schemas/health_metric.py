from pydantic import BaseModel, ConfigDict, Field
import datetime

class HealthMetricOutputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    metric: str = Field(max_length=50)
    user_tg_id: str = Field(max_length=50)
    value: float
    date: datetime.date

class HealthMetricInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    metric: str = Field(max_length=50)
    value: float
    date: datetime.date
