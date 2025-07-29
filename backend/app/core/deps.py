# app/core/deps.py

from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import current_user
from app.core.enums import UserRole
from app.db import get_session
from app.models.user import User


def get_db(session: Session = Depends(get_session)) -> Generator[Session, None, None]:
	yield session


async def current_gm(user: User = Depends(current_user)) -> User:
	if user.role != UserRole.gm:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="GM only")
	return user


async def current_organizer(user: User = Depends(current_user)) -> User:
	if user.role != UserRole.organizer:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Organizers only")
	return user
