from app.api.routes import players
from fastapi import FastAPI

app = FastAPI()

app.include_router(players.router, prefix="/players", tags=["Players"])
# app.include_router(games.router, prefix="/games", tags=["Games"])
