from collections import Counter
from datetime import date, datetime
from typing import Optional

from app.core.enums import GameRole, GameState
from pydantic import BaseModel, field_validator, model_validator


class GamePlayer(BaseModel):
    seat_no: int
    player_id: int
    fouls_count: int = 0
    removed: bool = False
    total_points: float = 0.0
    role: GameRole


class GameBase(BaseModel):
    id: int
    date: date
    players_qty: int
    state: GameState
    gm_id: int


class GameInProgress(GameBase):
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    players: list[GamePlayer]


class GameFinished(GameBase):
    started_at: datetime
    finished_at: datetime
    players: list[GamePlayer]

    @model_validator(mode="after")
    def check_roles(cls, model):
        roles_amount = Counter(p.role for p in model.players)
        if roles_amount[GameRole.sheriff] != 1:
            raise ValueError("There must be exactly 1 sheriff")
        if roles_amount[GameRole.don] != 1:
            raise ValueError("There must be exactly 1 don")
        mafia = roles_amount[GameRole.mafia] + roles_amount[GameRole.don]
        city = roles_amount[GameRole.citizen] + roles_amount[GameRole.sheriff]
        if mafia not in {2, 3}:
            raise ValueError("Total mafia (don + mafias) must be 2 or 3")
        if mafia == 2 and city != 6 and city != 5:
            raise ValueError(
                f"There can't be 2 mafias and {roles_amount[GameRole.citizen] + roles_amount[GameRole.sheriff]} citizens"
            )
        if mafia == 3 and (
            roles_amount[GameRole.citizen] != 6 and roles_amount[GameRole.citizen] != 5
        ):
            raise ValueError(
                f"There can't be 3 mafias and {roles_amount[GameRole.citizen] + roles_amount[GameRole.sheriff]} citizens"
            )
        if city + mafia != model.players_qty:
            raise ValueError("Sum of roles doesn't match players_qty")
        return model


class GameCreate(BaseModel):
    players_qty: int = 10
    rule_set_id: int

    @field_validator("players_qty")
    def qty_must_be_valid(cls, v):
        if not (7 <= v <= 10):
            raise ValueError("players_qty must be between 7 and 10")
        return v
