import datetime
import uuid

import httpx
from starlette import status

import src.database.models as src_models


class TestAddBookingHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/booking"

    async def test_base_scenario(
        self,
        client: httpx.AsyncClient,
        hotel: src_models.Hotel,
    ):
        payload = {
            "hotel_id": str(hotel.hotel_id),
            "date_start": str(datetime.date.today()),
            "date_end": str(datetime.date.today() + datetime.timedelta(days=3)),
        }

        response = await client.post(url=self.get_url(), json=payload)
        assert response.status_code == status.HTTP_201_CREATED

        response_data = response.json()
        assert "booking_id" in response_data

    async def test_missing_field(
        self,
        client: httpx.AsyncClient,
        hotel: src_models.Hotel,
    ):
        payload = {
            "hotel_id": str(hotel.hotel_id),
            "date_start": str(datetime.date.today()),
        }

        response = await client.post(url=self.get_url(), json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_non_existing_hotel(self, client: httpx.AsyncClient):
        payload = {
            "hotel_id": str(uuid.uuid4()),
            "date_start": str(datetime.date.today()),
            "date_end": str(datetime.date.today() + datetime.timedelta(days=2)),
        }

        response = await client.post(url=self.get_url(), json=payload)
        assert response.status_code == status.HTTP_404_NOT_FOUND
