import fastapi

import src.presentation.api as api


def setup_routers(app: fastapi.FastAPI):
    for router in api.v1_routers:
        app.include_router(router, prefix="/api/v1")
