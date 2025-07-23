from contextlib import asynccontextmanager

import uvicorn
from app.api.routes.players import router as players_router
from app.core.config import get_settings
from app.db import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.api.routes.games   import router as games_router
# from app.api.routes.stats   import router as stats_router
# from app.api.routes.events  import router as events_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # → код до старта приложения
    # например, создаём таблицы (dev/staging)
    await init_db()
    yield
    # ← код при выключении (если нужен)


app = FastAPI(
    title="Mafia Club API",
    version="0.1.0",
    lifespan=lifespan,  # подключаем менеджер
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде поставьте свои хосты
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ваши роутеры
app.include_router(players_router, prefix="/players", tags=["Players"])
# app.include_router(games_router, prefix="/games",   tags=["Games"])
# app.include_router(stats_router, prefix="/stats",   tags=["Stats"])
# app.include_router(events_router, prefix="/events",  tags=["Events"])

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
