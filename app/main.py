from fastapi import FastAPI
from app.routes import players, games

app = FastAPI()

app.include_router(players.router, prefix="/players", tags=["Players"])
app.include_router(games.router, prefix="/games", tags=["Games"])
