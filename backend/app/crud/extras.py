from __future__ import annotations

from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.extras import ExtraPoints
from app.models.game import GamePlayer
from app.schemas.extras import ExtraPointsCreate, ExtraPointsUpdate


# ───────────── CREATE ─────────────
def create(session: Session, data: ExtraPointsCreate, *, user_id: UUID) -> ExtraPoints:
	# валидация существования game_player
	gp = session.get(GamePlayer, data.game_player_id)
	if gp is None:
		raise ValueError("GamePlayer not found")

	obj = ExtraPoints(
		game_player_id=data.game_player_id,
		delta=data.delta,
		reason=data.reason,
		created_by=user_id,
	)
	session.add(obj)
	session.commit()
	session.refresh(obj)
	return obj


# ───────────── READ ─────────────
def get(session: Session, extra_id: int) -> Optional[ExtraPoints]:
	return session.get(ExtraPoints, extra_id)


def list_by_game(session: Session, game_id: int) -> Sequence[ExtraPoints]:
	stmt = (
		select(ExtraPoints)
		.join(GamePlayer, GamePlayer.id == ExtraPoints.game_player_id)
		.where(GamePlayer.game_id == game_id)
		.order_by(ExtraPoints.created_at.asc())
	)
	return session.execute(stmt).scalars().all()


# ───────────── UPDATE ─────────────
def update(session: Session, extra_id: int, data: ExtraPointsUpdate) -> Optional[ExtraPoints]:
	obj = session.get(ExtraPoints, extra_id)
	if obj is None:
		return None

	payload = data.model_dump(exclude_unset=True)
	for k, v in payload.items():
		setattr(obj, k, v)

	session.commit()
	session.refresh(obj)
	return obj


# ───────────── DELETE ─────────────
def delete(session: Session, extra_id: int) -> bool:
	obj = session.get(ExtraPoints, extra_id)
	if obj is None:
		return False
	session.delete(obj)
	session.commit()
	return True
