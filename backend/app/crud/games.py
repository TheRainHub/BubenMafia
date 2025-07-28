"""CRUD‑layer for Game (чистая работа с БД, без бизнес‑логики)."""

from __future__ import annotations

import datetime as dt
from typing import Any, Optional, Sequence, cast
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, selectinload

from app.core.enums import GameState
from app.models.game import Game
from app.schemas.games import GameCreate


# ───────────────────────────── CREATE ──────────────────────────────
def create(session: Session, game_in: GameCreate, gm_id: UUID) -> Game:
	obj = Game(**game_in.model_dump(), gm_id=gm_id, state=GameState.draft)
	session.add(obj)
	session.commit()
	session.refresh(obj)
	return obj


# ────────────────────────────── READ ───────────────────────────────
def get(
		session: Session,
		game_id: int,
		*,
		with_players: bool = False,
) -> Optional[Game]:
	if not with_players:
		# .get() → Any; подсказываем mypy через cast
		return cast(Optional[Game], session.get(Game, game_id))

	stmt = (
		select(Game)
		.filter_by(id=game_id)  # избегаем "bool vs ColumnElement"
		.options(selectinload(Game.players))
	)
	return cast(Optional[Game], session.scalar(stmt))


def list_games(
		session: Session,
		*,
		skip: int = 0,
		limit: int = 100,
) -> Sequence[Game]:
	gtbl = Game.__table__.c
	stmt = (
		select(Game)
		.order_by(
			desc(cast(Any, gtbl.date)),  # type stubs think .date is python date
			desc(cast(Any, gtbl.id)),
		)
		.offset(skip)
		.limit(limit)
	)
	return cast(Sequence[Game], session.scalars(stmt).all())


# ───────────────────────────── UPDATE ──────────────────────────────
def update_state(
		session: Session,
		game_id: int,
		new_state: GameState,
		*,
		finished_at: dt.datetime | None = None,
		aborted: bool | None = None,
) -> Optional[Game]:
	obj = cast(Optional[Game], session.get(Game, game_id))
	if obj is None:
		return None

	obj.state = new_state
	if finished_at is not None:
		obj.finished_at = finished_at
	if aborted is not None:
		obj.aborted = aborted

	session.add(obj)
	session.commit()
	session.refresh(obj)
	return obj


# ───────────────────────────── DELETE ──────────────────────────────
def delete(session: Session, game_id: int) -> bool:
	obj = cast(Optional[Game], session.get(Game, game_id))
	if obj is None:
		return False
	session.delete(obj)
	session.commit()
	return True
