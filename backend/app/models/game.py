import datetime as dt
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from app.core.enums import GameRole, GameState
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.event import GameEvent, VoteRound
    from app.models.extras import ExtraPoints, GameAudit
    from app.models.player import Player
    from app.models.rule import RuleSet


class Game(SQLModel, table=True):
    __table_args__ = (
        CheckConstraint("players_qty BETWEEN 7 AND 10", name="ck_players_qty_7_10"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    players_qty: int = Field(default=10)
    rule_set_id: int = Field(foreign_key="ruleset.id")
    gm_id: UUID = Field(foreign_key="user.id")
    state: GameState = Field(default=GameState.draft)
    date: dt.date = Field(default_factory=dt.date.today)
    started_at: dt.datetime | None = Field(default=None)
    finished_at: dt.datetime | None = Field(default=None)
    aborted: bool = Field(default=False)

    rule_set: Mapped[Optional["RuleSet"]] = Relationship(back_populates="games")
    players: Mapped[list["GamePlayer"]] = Relationship(back_populates="game")
    events: Mapped[list["GameEvent"]] = Relationship(
        back_populates="game", sa_relationship_kwargs={"lazy": "selectin"}
    )
    vote_rounds: Mapped[list["VoteRound"]] = Relationship(back_populates="game")
    audits: Mapped[list["GameAudit"]] = Relationship(back_populates="game")


class GamePlayer(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("game_id", "seat_no", name="uq_game_seat"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    player_id: int = Field(foreign_key="player.id")
    seat_no: int = Field(nullable=False)
    role: GameRole = Field(default=GameRole.citizen)
    fouls_count: int = Field(default=0)
    removed: bool = Field(default=False)
    total_points: float = Field(default=0.0)

    game: Mapped[Optional["Game"]] = Relationship(back_populates="players")
    player: Mapped[Optional["Player"]] = Relationship(back_populates="games")
    extra_points: Mapped[List["ExtraPoints"]] = Relationship(
        back_populates="game_player",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
