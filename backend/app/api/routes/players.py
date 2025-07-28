from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.deps import current_gm, get_db
from app.crud import players as crud
from app.schemas.players import PlayerCreate, PlayerRead, PlayerUpdate

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
def create_player(
    payload: PlayerCreate,
    session: Session = Depends(get_db),
):
    try:
        return crud.create(session, payload, registered=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/quick",
    response_model=PlayerRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_gm)],
)
def quick_add_player(
    nickname: str,
    session: Session = Depends(get_db),
):
    try:
        return crud.quick_add(session, nickname)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{player_id}", response_model=PlayerRead)
def update_player(
    player_id: int,
    payload: PlayerUpdate,
    session: Session = Depends(get_db),
    user_id: UUID | None = Depends(current_gm),  # временно: разрешаем GM редактировать
):
    player = crud.update(session, player_id, payload)
    if not player:
        raise HTTPException(404, "Player not found")
    return player
