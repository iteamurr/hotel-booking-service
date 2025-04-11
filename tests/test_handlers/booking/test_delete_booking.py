from starlette import status
import httpx

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
