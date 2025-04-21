import fastapi

import src.presentation.api.routes as api_routes


def setup_routers(app: fastapi.FastAPI):
    for router in api_routes.v1_routers:
        app.include_router(router, prefix="/api/v1")
