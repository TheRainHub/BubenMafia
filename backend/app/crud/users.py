from typing import Optional
from uuid import UUID

from sqlmodel import Session

from app.models.user import User


def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
    """
    Возвращает User по его UUID или None, если не найден.
    """
    return session.get(User, user_id)
