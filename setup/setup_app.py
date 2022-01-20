import os

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from db import database
from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend
from dotenv import load_dotenv


def create_app():
    """
    This function is used to create, configure and return the FastAPI app object.
    :return: FastAPI app object
    """
    app_path = os.path.dirname(os.path.abspath(__file__))
    project_folder = os.path.expanduser(app_path)
    load_dotenv(os.path.join(project_folder, '.env'))  # load the content of the .env as environment var

    db = database.Base.metadata.create_all(bind=database.engine)
    # print(f"Created {len(database.engine.table_names())} tables: {database.engine.table_names()}")
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=['http://127.0.0.1:8080'],
        allow_methods=["GET", 'POST'],
        allow_headers=["Access-Control-Allow-Origin"],
    )

    @app.on_event('startup')
    async def on_startup() -> None:
        rc = RedisCacheBackend('redis://')
        caches.set(CACHE_KEY, rc)

    @app.on_event('shutdown')
    async def on_shutdown() -> None:
        await close_caches()

    static_folder = app_path.split('/setup')[0] + '/static'
    app.mount("/static", StaticFiles(directory=static_folder), name="static")
    app.include_router(api_router)
    app.add_middleware(DBSessionMiddleware, db_url="sqlite://")

    return app
