from typing import Optional, Sequence, cast
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models.player import Player
from app.schemas.players import PlayerCreate, PlayerUpdate


# ────────────────── CREATE ──────────────────
def create(
    session: Session,
    data: PlayerCreate,
    *,
    user_id: UUID | None = None,
    registered: bool = False,
) -> Player:
    obj = Player(
        nickname=data.nickname,
        email=data.email,
        avatar_url=data.avatar_url,
        user_id=user_id,
        is_registered=registered,
    )
    session.add(obj)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise ValueError("Nickname already exists") from exc
    session.refresh(obj)
    return obj


def quick_add(session: Session, nickname: str) -> Player:
    return create(session, PlayerCreate(nickname=nickname), registered=False)


# ─────────────────── READ ───────────────────
def get(session: Session, player_id: int) -> Optional[Player]:
    return session.get(Player, player_id)


def get_by_nickname(session: Session, nickname: str) -> Optional[Player]:
    stmt = select(Player).where(Player.nickname == nickname)
    return session.exec(stmt).first()


def list_players(
    session: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[Player]:
    stmt = select(Player).offset(skip).limit(limit)
    return session.exec(stmt).all()


# ────────────────── UPDATE ──────────────────
def update(session: Session, player_id: int, data: PlayerUpdate) -> Optional[Player]:
    obj = session.get(Player, player_id)
    if obj is None:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    session.commit()
    session.refresh(obj)
    return cast(Player, obj)


# ────────────────── DELETE ──────────────────
def delete(session: Session, player_id: int) -> bool:
    obj = session.get(Player, player_id)
    if not obj:
        return False
    session.delete(obj)
    session.commit()
    return True
