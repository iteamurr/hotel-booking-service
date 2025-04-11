from src.api.v1.booking import router as booking_router
from src.api.v1.hotel import router as hotel_router

v1_routers = [hotel_router, booking_router]

# For a future use
v2_routers = []

all = [v1_routers, v2_routers]
