import fastapi
import uvicorn

import src.config as config


def get_app() -> fastapi.FastAPI:
    settings = config.get_api_settings()

    app = fastapi.FastAPI(title=settings.title)

    config.setup_routers(app)
    return app


if __name__ == "__main__":
    settings = config.get_api_settings()

    app = get_app()

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
    )
