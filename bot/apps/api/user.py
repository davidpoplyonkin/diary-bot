from .base import BaseAPIClient
from schemas import UserInputSchema, UserOutputSchema

class UserClient(BaseAPIClient):
    async def get_user(self, tg_id: str) -> UserOutputSchema | None:
        response = await self.client.get(f"/users/{tg_id}")

        if response.status_code == 404:
            return None
        
        response.raise_for_status()

        return UserOutputSchema(**response.json())
    
    async def upsert_user(self, tg_id: str, full_name: str) -> UserOutputSchema:
        user = UserInputSchema(tg_id=tg_id, full_name=full_name)

        response = await self.client.put(f"/users/{tg_id}", json=user.dict())

        response.raise_for_status()

        return UserOutputSchema(**response.json())
    
    async def blacklist_user(self, tg_id: str) -> UserOutputSchema | None:
        response = await self.client.post(f"/users/{tg_id}/blacklist")

        if response.status_code == 404:
            return None
        
        response.raise_for_status()

        return UserOutputSchema(**response.json())
