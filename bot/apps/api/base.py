import httpx

from globals import API_KEY, API_URL

class HeaderInterceptor(httpx.Auth):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def auth_flow(self, request):
        # Attach the API key to the request headers
        request.headers["X-Api-Key"] = self.api_key

        yield request

class BaseAPIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=API_URL,
            auth=HeaderInterceptor(API_KEY)
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
