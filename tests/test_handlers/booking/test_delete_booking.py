import uuid

import httpx
from starlette import status

import tests.utils as tests_utils


class TestDeleteBookingHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/booking/{0}"

    async def test_base_scenario(
        self,
        client: httpx.AsyncClient,
        booking_factory: tests_utils.HotelBookingFactory,
    ):
        booking = await booking_factory.make_booking()
        response = await client.delete(url=self.get_url().format(booking.booking_id))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_deleting_missing_booking(self, client: httpx.AsyncClient):
        response = await client.delete(url=self.get_url().format(str(uuid.uuid4())))
        assert response.status_code == status.HTTP_404_NOT_FOUND
