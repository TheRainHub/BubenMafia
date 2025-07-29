from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.core.auth import current_user
from app.crud.users import get as get_user_by_id  # вам понадобится CRUD‑функция для юзеров
from app.db import get_session
from app.models.user import User  # поправьте путь, если у вас модель лежит в другом месте


def get_db(session: Session = Depends(get_session)) -> Session:
	"""
	Общая зависимость для доступа к сессии БД.
	Теперь её можно юзать во всех роутерах.
	"""
	return session


def current_gm(session: Session = Depends(get_db), user_id: UUID = Depends(), ) -> User:
	"""
	Заглушка: получает текущего залогиненного пользователя,
	проверяет, что это GM, и возвращает его модель.
	Пока у вас нет полноценного auth‑конфигурации, вы можете
	временно просто return user или бросать 403, если нужно.
	"""
	user = get_user_by_id(session, user_id)
	if not user or user.role != "gm":
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только GM может выполнять эту операцию", )
	return user


def current_organizer(
		session: Session = Depends(get_db),
		user_id: UUID = Depends(current_user),  # fastapi‑users
) -> User:
	user = get_user_by_id(session, user_id)
	if not user or user.role != "organizer":
		raise HTTPException(status_code=403, detail="Organizers only")
	return user
