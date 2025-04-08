import fastapi
import uvicorn

import src.config as config


if __name__ == "__main__":
    settings = config.get_api_settings()

    app = fastapi.FastAPI(
        title=settings.title,
    )

    config.setup_routers(app)

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
    )
