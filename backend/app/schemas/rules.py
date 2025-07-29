from decimal import Decimal
from typing import Annotated, Optional, List

from pydantic import BaseModel, Field, ConfigDict

Delta = Annotated[
	Decimal,
	Field(
		ge=Decimal("0"),  # >= 0
		le=Decimal("99.9"),  # опционально верхний предел
		max_digits=4,
		decimal_places=2,
		description="Очки: до 2 десятичных знаков",
	),
]


# ─────────── RULE ITEM ───────────
class RuleItemBase(BaseModel):
	condition: str = Field(..., examples=["CITY_WIN"])
	role_filter: Optional[str] = Field(
		None, examples=["Citizen", "Mafia", None]
	)
	delta: Delta


class RuleItemCreate(RuleItemBase):
	pass


class RuleItemUpdate(BaseModel):
	condition: Optional[str] = None
	role_filter: Optional[str] = None
	delta: Optional[Delta] = None


class RuleItemRead(RuleItemBase):
	id: int
	rule_set_id: int

	model_config = ConfigDict(from_attributes=True)


# ─────────── RULE SET ───────────
class RuleSetBase(BaseModel):
	name: str


class RuleSetCreate(RuleSetBase):
	is_active: bool = False
	items: List[RuleItemCreate] = []


class RuleSetUpdate(BaseModel):
	name: Optional[str] = None
	is_active: Optional[bool] = None


class RuleSetRead(RuleSetBase):
	id: int
	is_active: bool
	items: List[RuleItemRead] = []

	model_config = ConfigDict(from_attributes=True)
