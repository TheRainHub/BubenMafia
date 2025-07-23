from typing import TYPE_CHECKING

from app.core.enums import UserRole
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from app.models.extras import GameAudit
    from app.models.player import Player


class User(SQLModelBaseUserDB, table=True):
    __tablename__ = "user"

    role: UserRole = Field(
        sa_column=Column(
            SQLEnum(UserRole, name="role_enum", native_enum=False),
            nullable=False,
            default=UserRole.player,
        ),
        description="Организатор / GM / Player",
    )

    players: Mapped[list["Player"]] = Relationship(back_populates="user")
    audits: Mapped[list["GameAudit"]] = Relationship(back_populates="user")
