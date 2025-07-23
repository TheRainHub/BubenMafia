from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.game import Game, GamePlayer
    from app.models.user import User


class ExtraPoints(SQLModel, table=True):
    """
    Ручные «дополнительные» очки для игрока.
    Используется организатором, если нужно выдать бонус/штраф.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    game_player_id: int = Field(foreign_key="gameplayer.id", nullable=False)
    delta: float = Field(nullable=False, description="Плюс/минус очков")
    reason: str = Field(nullable=True, max_length=255, description="Причина изменения")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    # связи
    game_player: Mapped[Optional["GamePlayer"]] = Relationship(
        back_populates="extra_points"
    )


class GameAudit(SQLModel, table=True):
    """
    Лог изменений завершённой игры (или админ-правок в stats).
    Хранит, кто и когда что поменял.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id", nullable=False)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    field: str = Field(
        nullable=False, max_length=64, description="Имя поля, которое поменяли"
    )
    old_value: str = Field(nullable=True, description="Старое значение")
    new_value: str = Field(nullable=True, description="Новое значение")
    ts: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

    # связи
    game: Mapped[Optional["Game"]] = Relationship(back_populates="audits")
    user: Mapped[Optional["User"]] = Relationship(back_populates="audits")
