import httpx
import pytest
from starlette import status

import src.schemas.hotel as hotel_schemas
import tests.utils as tests_utils


class TestGetHotelListHandler:
    @staticmethod
    def get_url() -> str:
        return "/api/v1/hotel/list"

    async def test_base_scenario(
        self,
        client: httpx.AsyncClient,
        hotel_factory: tests_utils.HotelFactory,
    ):
        hotel1 = await hotel_factory.make_hotel()
        hotel2 = await hotel_factory.make_hotel()

        response = await client.get(url=self.get_url())
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert len(response_data) == 2

        expected = sorted([hotel1, hotel2], key=lambda x: x.date_created)
        assert response_data[0]["hotel_id"] == str(expected[0].hotel_id)
        assert response_data[1]["hotel_id"] == str(expected[1].hotel_id)

    @pytest.mark.parametrize(
        "order",
        [
            hotel_schemas.HotelOrder(order_by="cost", descending=True),
            hotel_schemas.HotelOrder(order_by="cost", descending=False),
            hotel_schemas.HotelOrder(order_by="date_created", descending=True),
            hotel_schemas.HotelOrder(order_by="date_created", descending=False),
        ],
    )
    async def test_order_by_scenario(
        self,
        client: httpx.AsyncClient,
        hotel_factory: tests_utils.HotelFactory,
        order: hotel_schemas.HotelOrder,
    ):
        params = {"order_by": order.order_by.name, "descending": order.descending}

        hotel1 = await hotel_factory.make_hotel()
        hotel2 = await hotel_factory.make_hotel()

        response = await client.get(url=self.get_url(), params=params)
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert len(response_data) == 2

        expected = sorted(
            [hotel1, hotel2],
            key=lambda x: getattr(x, order.order_by),
            reverse=order.descending,
        )
        assert response_data[0]["hotel_id"] == str(expected[0].hotel_id)
        assert response_data[1]["hotel_id"] == str(expected[1].hotel_id)
