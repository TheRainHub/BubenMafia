from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.core.deps import current_gm, get_db
from app.crud import extras as crud
from app.schemas.extras import (ExtraPointsCreate, ExtraPointsRead,
								ExtraPointsUpdate)

router = APIRouter(prefix="/extras", tags=["extras"])


def gm_or_org(user_id: UUID = Depends(current_gm), session: Session = Depends(get_db)) -> UUID:
	# Current_gm уже проверяет роль "gm".
	# Разрешим и организатора: если current_gm бросил 403, FastAPI не дойдёт сюда.
	# Альтернатива — отдельная зависимость, которая принимает любую из двух ролей.
	return user_id


@router.post("/", response_model=ExtraPointsRead, status_code=status.HTTP_201_CREATED)
def create_extra(
		payload: ExtraPointsCreate,
		session: Session = Depends(get_db),
		user_id: UUID = Depends(gm_or_org),
):
	try:
		obj = crud.create(session, payload, user_id=user_id)
		return obj
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ExtraPointsRead])
def list_extras(
		game_id: int = Query(..., description="Фильтрация по игре"),
		session: Session = Depends(get_db),
) -> Sequence[ExtraPointsRead]:
	return crud.list_by_game(session, game_id)


@router.patch("/{extra_id}", response_model=ExtraPointsRead)
def update_extra(
		extra_id: int,
		payload: ExtraPointsUpdate,
		session: Session = Depends(get_db),
		_: UUID = Depends(gm_or_org),
):
	obj = crud.update(session, extra_id, payload)
	if obj is None:
		raise HTTPException(status_code=404, detail="ExtraPoints not found")
	return obj


@router.delete("/{extra_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_extra(
		extra_id: int,
		session: Session = Depends(get_db),
		_: UUID = Depends(gm_or_org),
):
	ok = crud.delete(session, extra_id)
	if not ok:
		raise HTTPException(status_code=404, detail="ExtraPoints not found")
