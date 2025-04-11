from starlette import status
import httpx

import tests.utils as tests_utils


class TestGetBookingListHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/booking/{0}/list"

    async def test_base_scenario(
        self,
        client: httpx.AsyncClient,
        booking_factory: tests_utils.HotelBookingFactory,
    ):
        booking1 = await booking_factory.make_booking()
        booking2 = await booking_factory.make_booking()

        response = await client.get(url=self.get_url().format(booking_factory.hotel_id))
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert len(response_data) == 2

        expected = sorted([booking1, booking2], key=lambda x: x.date_start)
        assert response_data[0]["booking_id"] == str(expected[0].booking_id)
        assert response_data[1]["booking_id"] == str(expected[1].booking_id)
