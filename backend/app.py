# app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.db import init_db
from src.api.health import router as health_router
from src.api.auth import router as auth_router
from src.api.game import router as game_router
from src.api.matchup import router as matchup_router
from src.constants.fastapi import FASTAPI_TITLE, FASTAPI_VERSION, VALID_ORIGINS


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
        await init_db()

    app.include_router(health_router, prefix='/api')
    app.include_router(auth_router, prefix='/api')
    app.include_router(game_router, prefix='/api')
    app.include_router(matchup_router, prefix='/api')

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
