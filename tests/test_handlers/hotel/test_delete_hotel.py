import httpx
from starlette import status

import src.database.models as src_models
import tests.utils as tests_utils


class TestDeleteHotelHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/hotel/{0}"

    async def test_base_scenario(
        self,
        client: httpx.AsyncClient,
        hotel: src_models.Hotel,
        booking_factory: tests_utils.HotelBookingFactory,
    ):
        booking_factory.hotel_id = hotel.hotel_id
        _ = await booking_factory.make_booking()

        response = await client.delete(url=self.get_url().format(hotel.hotel_id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
