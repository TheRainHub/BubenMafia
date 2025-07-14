from fastapi import FastAPI
from backend.app.routes import games, players

app = FastAPI()

app.include_router(players.router, prefix="/players", tags=["Players"])
app.include_router(games.router, prefix="/games", tags=["Games"])
