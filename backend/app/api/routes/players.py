from app.db import get_session
from app.models.player import Player
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

router = APIRouter(tags=["players"])


@router.get("/", response_model=list[Player])
def list_players(
    skip: int = 0,
    limit: int = 50,
    session: Session = Depends(get_session),  # <—
):
    players = session.exec(select(Player).offset(skip).limit(limit)).all()
    return players


@router.get("/{player_id}", response_model=Player)
def get_player(
    player_id: int,
    session: Session = Depends(get_session),  # <—
):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
