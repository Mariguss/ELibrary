from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.api.pages import router as pages_router
from app.api.v1.routes import routers as v1_routers
from app.core.config import configs
from app.core.container import Container
import os


def create_app() -> FastAPI:
    container = Container()
    app = FastAPI(
        title=configs.PROJECT_NAME,
        version="1.0.0",
    )
    app.container = container

    if configs.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    static_dir = os.path.join(configs.PROJECT_ROOT, "static")
    os.makedirs(static_dir, exist_ok=True)
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    uploads_dir = os.path.join(configs.PROJECT_ROOT, "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

    app.include_router(v1_routers, prefix=configs.API_V1_STR)
    app.include_router(pages_router)

    return app


app = create_app()