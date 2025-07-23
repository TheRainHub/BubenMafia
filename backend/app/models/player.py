from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import Mapped
from sqlmodel import CheckConstraint, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.game import GamePlayer
    from app.models.user import User


class Player(SQLModel, table=True):
    """
    Игрок — сущность публичной статистики.
    Может быть «незарегистрированным», пока пользователь не привяжет e‑mail.
    """

    __table_args__ = (
        CheckConstraint(
            "(is_registered) OR (email IS NULL)",  # незарегистрированный — без email
            name="ck_player_email_null_when_unregistered",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: str = Field(
        sa_type=CITEXT, nullable=False, unique=True, index=True, max_length=32
    )

    email: Optional[str] = Field(default=None, max_length=255)
    avatar_url: Optional[str] = Field(default=None, max_length=512)
    user_id: Optional[UUID] = Field(
        default=None, foreign_key="user.id"
    )  # fastapi‑users
    is_registered: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # связи
    games: Mapped[list["GamePlayer"]] = Relationship(back_populates="player")
    user: Mapped[Optional["User"]] = Relationship(back_populates="players")
