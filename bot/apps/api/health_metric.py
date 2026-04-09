import datetime

from .base import BaseAPIClient
from schemas import HealthMetricOutputSchema

class HealthMetricClient(BaseAPIClient):
    async def get_metric(
        self,
        user_tg_id: str,
        metric: str,
        date: str
    ) -> HealthMetricOutputSchema | None:
        response = await self.client.get(
            f"/users/{user_tg_id}/metrics/{metric}/{date}"
        )

        if response.status_code == 404:
            return None
        
        response.raise_for_status()

        return HealthMetricOutputSchema(**response.json())
    
    async def bulk_insert_metrics(
        self,
        user_tg_id: str,
        metrics: list[dict]
    ) -> None:
        response = await self.client.post(
            f"/users/{user_tg_id}/metrics/bulk",
            json=metrics
        )

        response.raise_for_status()
