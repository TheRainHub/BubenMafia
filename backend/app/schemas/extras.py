from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ExtraPointsCreate(BaseModel):
	game_player_id: int
	delta: float  # может быть отрицательным
	reason: str = Field(min_length=1, max_length=255)


class ExtraPointsUpdate(BaseModel):
	delta: Optional[float] = None
	reason: Optional[str] = Field(default=None, min_length=1, max_length=255)


class ExtraPointsRead(BaseModel):
	id: int
	game_player_id: int
	delta: float
	reason: str
	created_by: UUID
	created_at: datetime

	model_config = ConfigDict(from_attributes=True)
