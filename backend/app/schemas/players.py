from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl


class _PlayerBase(BaseModel):
    nickname: str
    avatar_url: Optional[HttpUrl] = None


class PlayerCreate(_PlayerBase):
    email: Optional[EmailStr] = None  # для self‑signup (может быть пусто при quick‑add)


class PlayerUpdate(BaseModel):
    email: Optional[EmailStr] = None
    avatar_url: Optional[HttpUrl] = None


class PlayerRead(_PlayerBase):
    id: int
    email: Optional[EmailStr] = None
    user_id: Optional[UUID] = None
    is_registered: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
