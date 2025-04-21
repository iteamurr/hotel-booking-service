import fastapi
import uvicorn

import src.infrastructure.config.dependencies as config_depends
import src.infrastructure.config.setups as config_setups


def get_app() -> fastapi.FastAPI:
    settings = config_depends.get_api_settings()

    app = fastapi.FastAPI(title=settings.title)

    config_setups.setup_routers(app)
    return app


if __name__ == "__main__":
    settings = config_depends.get_api_settings()

    app = get_app()

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
    )
