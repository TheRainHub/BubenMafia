from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from app.core.enums import Condition, GameRole
from pydantic import ConfigDict
from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from app.models.game import Game


class RuleSet(SQLModel, table=True):
    """
    Набор правил (versioned). Один активный по умолчанию.
    """

    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=64, unique=True)
    is_active: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # связи
    items: Mapped[list["RuleItem"]] = Relationship(back_populates="rule_set")
    games: Mapped[list["Game"]] = Relationship(back_populates="rule_set")


class RuleItem(SQLModel, table=True):
    """
    Одна строка таблицы начисления очков.
    Пример: CITY_WIN + Citizen → +3 очка.
    """

    model_config = ConfigDict(from_attributes=True)
    __table_args__ = (
        UniqueConstraint(
            "rule_set_id", "condition", "role_filter", name="uq_ruleitem_unique_triplet"
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    rule_set_id: int = Field(foreign_key="ruleset.id")
    condition: Condition = Field(
        sa_column=Column(
            SQLEnum(Condition, name="condition_enum", native_enum=False), nullable=False
        )
    )
    role_filter: Optional[GameRole] = Field(default=None)  # None = *any*
    delta: float = Field(nullable=False)

    rule_set: Mapped[Optional[RuleSet]] = Relationship(back_populates="items")
