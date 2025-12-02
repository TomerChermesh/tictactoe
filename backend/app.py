# app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.db import init_db
from src.api.health import router as health_router
from src.api.auth import router as auth_router
from src.api.games import router as games_router
from src.api.matchups import router as matchups_router
from src.constants.fastapi import FASTAPI_TITLE, FASTAPI_VERSION, VALID_ORIGINS
from src.utils.logger import logger


def create_app() -> FastAPI:
    app = FastAPI(title=FASTAPI_TITLE, version=FASTAPI_VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=VALID_ORIGINS,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    @app.on_event('startup')
    async def on_startup():
        logger.info('Starting application...')
        try:
            await init_db()
            logger.info('Database initialized successfully')
        except Exception as e:
            logger.critical('Failed to initialize database', exception=e)
            raise
        logger.info(f'Application started: {FASTAPI_TITLE} v{FASTAPI_VERSION}')

    app.include_router(health_router, prefix='/api')
    app.include_router(auth_router, prefix='/api')
    app.include_router(games_router, prefix='/api')
    app.include_router(matchups_router, prefix='/api')

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
