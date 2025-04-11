import httpx
from starlette import status


class TestAddHotelHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/hotel"

    async def test_base_scenario(self, client: httpx.AsyncClient):
        payload = {"description": "First Hotel", "cost": 199.89}

        response = await client.post(url=self.get_url(), json=payload)
        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert "hotel_id" in response_data

    async def test_missing_field(self, client: httpx.AsyncClient):
        payload = {"description": "First Hotel"}

        response = await client.post(url=self.get_url(), json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
