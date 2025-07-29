from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi_users import schemas as fu_schemas
from pydantic import ConfigDict

from app.core.enums import UserRole


class UserRead(fu_schemas.BaseUser[UUID]):
	role: UserRole
	model_config = ConfigDict(from_attributes=True)


class UserCreate(fu_schemas.BaseUserCreate):
	role: UserRole


# при желании можно оставить json_schema_extra с примером


class UserUpdate(fu_schemas.BaseUserUpdate):
	role: Optional[UserRole] = None
	model_config = ConfigDict(extra="forbid", populate_by_name=True)
