from fastapi import APIRouter

from .players import router as players_router
# from .games import router as games_router
from .rules import router as rules_router

api_router = APIRouter()
api_router.include_router(players_router)
# api_router.include_router(games_router)
api_router.include_router(rules_router)
