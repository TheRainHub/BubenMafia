from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict, constr

from app.core.enums import UserRole


# ─── общее ──────────────────────────────────
class UserBase(BaseModel):
	email: EmailStr
	role: UserRole | str = Field(..., examples=["organizer", "gm", "player"])


# ─── read ───────────────────────────────────
class UserRead(UserBase):
	id: UUID
	is_active: bool
	is_superuser: bool
	is_verified: bool
	created_at: datetime

	model_config = ConfigDict(
		from_attributes=True,
		populate_by_name=True,  # snake_case ←→ camelCase, если надо
	)


# ─── create ─────────────────────────────────
class UserCreate(UserBase):
	password: constr(min_length=8, max_length=128)


# ─── update ─────────────────────────────────
class UserUpdate(BaseModel):
	email: EmailStr | None = None
	password: constr(min_length=8, max_length=128) | None = None
	role: UserRole | str | None = None
	is_active: bool | None = None
	is_superuser: bool | None = None
	is_verified: bool | None = None

	model_config = ConfigDict(
		extra="forbid",
		populate_by_name=True,
	)
