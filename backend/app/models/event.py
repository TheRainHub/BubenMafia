from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.game import Game


class EventType(SQLModel, table=True):
    """
    Справочник допустимых типов событий.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(
        sa_column=Column(String, unique=True, nullable=False),
        description="Уникальный код события, e.g. 'deal_roles'",
    )
    description: Optional[str] = Field(
        default=None, description="Человеко‑читаемое описание события"
    )

    events: Mapped[list["GameEvent"]] = Relationship(back_populates="event_type")


class GameEvent(SQLModel, table=True):
    """
    События живой игры со ссылкой на EventType.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    ts: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
            nullable=False,
        ),
    )
    event_type_id: int = Field(foreign_key="eventtype.id", nullable=False)
    payload: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON, nullable=False),
        description="Дополнительные данные события, структура зависит от type",
    )

    game: Mapped[Optional["Game"]] = Relationship(back_populates="events")
    event_type: Mapped[Optional[EventType]] = Relationship(back_populates="events")


class VoteRound(SQLModel, table=True):
    """
    Раунд голосования: указывает, какой по счёту, и собирает голоса.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    round_no: int = Field(
        nullable=False, description="Номер раунда голосования: 1, 2, …"
    )

    items: Mapped[list["VoteItem"]] = Relationship(back_populates="round")
    game: Mapped[Optional["Game"]] = Relationship(back_populates="vote_rounds")


class VoteItem(SQLModel, table=True):
    """
    Позиция в раунде голосования: кто выставлен (seat_no) и сколько голосов набрал.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    vote_round_id: int = Field(foreign_key="voteround.id")
    target_seat: int = Field(
        nullable=False, description="Кто выставлен на голосование (по seat_no)"
    )
    count: int = Field(default=0, description="Сколько голосов набрано")

    round: Mapped[Optional[VoteRound]] = Relationship(back_populates="items")
