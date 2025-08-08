from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.db import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
	if not settings.testing:
		await init_db()
	yield


# ← код при выключении (если нужен)


def create_app() -> FastAPI:
	app = FastAPI(title="Mafia Club API", version="0.1.0", lifespan=lifespan)

	app.include_router(api_router)

	# CORS
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)
	return app


if __name__ == "__main__":
	app = create_app()
	uvicorn.run(
		"app.main:app",
		host="0.0.0.0",
		port=8000,
		reload=True,
	)
