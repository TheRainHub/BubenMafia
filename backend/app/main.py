from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import *
from app.core.auth import fastapi_users, auth_backend
from app.core.config import get_settings
from app.db import init_db
from app.schemas.users import UserRead, UserCreate

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

app.include_router(
	fastapi_users.get_auth_router(auth_backend),
	prefix="/auth/jwt",
	tags=["auth"],
)
app.include_router(
	fastapi_users.get_register_router(UserRead, UserCreate),
	prefix="/auth",
	tags=["auth"],
)
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
