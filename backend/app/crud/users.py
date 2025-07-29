from __future__ import annotations

from typing import Optional, Sequence
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.models.user import User
from app.schemas.users import UserCreate, UserUpdate

# Настройка хеширования паролей (совместимо с fastapi-users по умолчанию)
_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─────────────────────────── helpers ───────────────────────────

def _hash_password(plain_password: str) -> str:
	return _pwd_ctx.hash(plain_password)


def _apply_update(obj: User, data: UserUpdate) -> None:
	"""Применяет частичное обновление к модели User"""
	update_data = data.model_dump(exclude_unset=True)
	password = update_data.pop("password", None)
	if password:
		obj.hashed_password = _hash_password(password)

	for k, v in update_data.items():
		# запрещаем прямую запись системных флагов, если нужно — вынеси в отдельные функции
		setattr(obj, k, v)


# ─────────────────────────── CREATE ───────────────────────────

def create(session: Session, data: UserCreate, *, is_active: bool = True, is_superuser: bool = False,
		   is_verified: bool = False) -> User:
	"""
	Создаёт пользователя, хеширует пароль, обрабатывает уникальность email/nickname.
	"""
	obj = User(email=data.email, role=data.role,  # строка или Enum — как в модели
			   hashed_password=_hash_password(data.password), is_active=is_active, is_superuser=is_superuser,
			   is_verified=is_verified, )
	session.add(obj)
	try:
		session.commit()
	except IntegrityError as exc:
		session.rollback()
		raise ValueError("Email уже занят") from exc
	session.refresh(obj)
	return obj


# ───────────────────────────── READ ────────────────────────────

def get(session: Session, user_id: UUID) -> Optional[User]:
	return session.get(User, user_id)


def get_by_email(session: Session, email: str) -> Optional[User]:
	stmt = select(User).where(User.email == email)
	return session.exec(stmt).scalars().first()


def list_users(session: Session, *, skip: int = 0, limit: int = 100) -> Sequence[User]:
	stmt = select(User).offset(skip).limit(limit)
	return session.exec(stmt).scalars().all()


# ─────────────────────────── UPDATE ────────────────────────────

def update(session: Session, user_id: UUID, data: UserUpdate) -> Optional[User]:
	"""
	Частичное обновление.
	Если пришёл password — хешируется.
	Для смены роли админом можно либо использовать это же поле role, либо сделать set_role().
	"""
	obj = session.get(User, user_id)
	if obj is None:
		return None

	_apply_update(obj, data)

	try:
		session.commit()
	except IntegrityError as exc:
		session.rollback()
		raise ValueError("Email или nickname уже заняты") from exc
	session.refresh(obj)
	return obj


def set_role(session: Session, user_id: UUID, role: str) -> Optional[User]:
	"""
	Админская операция — смена роли независимо от UserUpdate.
	"""
	obj = session.get(User, user_id)
	if obj is None:
		return None
	obj.role = role
	session.commit()
	session.refresh(obj)
	return obj


def set_active_flags(session: Session, user_id: UUID, *, is_active: Optional[bool] = None,
					 is_verified: Optional[bool] = None, is_superuser: Optional[bool] = None) -> Optional[User]:
	"""
	Админская операция — изменение системных флагов.
	"""
	obj = session.get(User, user_id)
	if obj is None:
		return None

	if is_active is not None:
		obj.is_active = is_active
	if is_verified is not None:
		obj.is_verified = is_verified
	if is_superuser is not None:
		obj.is_superuser = is_superuser

	session.commit()
	session.refresh(obj)
	return obj


# ─────────────────────────── DELETE ────────────────────────────

def delete(session: Session, user_id: UUID) -> bool:
	obj = session.get(User, user_id)
	if obj is None:
		return False
	session.delete(obj)
	session.commit()
	return True
