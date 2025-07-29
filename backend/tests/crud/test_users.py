from typing import cast
from uuid import uuid4

import pytest
from pydantic import EmailStr
from sqlmodel import Session

from app.core.enums import UserRole  # поправьте путь при необходимости
from app.crud import users as crud
from app.schemas.users import UserCreate, UserUpdate


def _mk_email() -> EmailStr:
	return cast(EmailStr, f"user_{uuid4().hex[:8]}@example.com")


def test_create_and_get_user(session: Session):
	email = _mk_email()
	plain_password = "StrongP@ssw0rd"

	u = crud.create(
		session,
		UserCreate(
			email=email,
			role=UserRole.gm,
			password=plain_password,
		),
		is_active=True,
		is_superuser=False,
		is_verified=False,
	)

	assert u.id is not None
	assert u.email == email
	assert u.role in (UserRole.gm, getattr(UserRole, "gm", None), "gm")
	assert hasattr(u, "hashed_password")
	assert u.hashed_password and u.hashed_password != plain_password

	by_id = crud.get(session, u.id)
	assert by_id and by_id.email == email

	by_email = crud.get_by_email(session, cast(str, email))
	assert by_email and by_email.id == u.id


def test_uniqueness_email(session: Session):
	email = _mk_email()

	crud.create(
		session,
		UserCreate(
			email=email,
			role=UserRole.player,
			password="Aaaaaaaa1!",
		),
	)

	# тот же email — конфликт
	with pytest.raises(ValueError):
		crud.create(
			session,
			UserCreate(
				email=email,  # тот же
				role=UserRole.player,
				password="Bbbbbbbb1!",
			),
		)


def test_update_user_profile_and_password(session: Session):
	u = crud.create(
		session,
		UserCreate(
			email=_mk_email(),
			role=UserRole.player,
			password="OldPassw0rd!",
		),
	)
	old_hash = u.hashed_password

	new_email = _mk_email()
	updated = crud.update(
		session,
		u.id,
		UserUpdate(
			email=new_email,
			password="NewPassw0rd!",
		),
	)

	assert updated is not None
	assert updated.email == new_email
	assert updated.hashed_password != old_hash


def test_set_role_and_flags(session: Session):
	u = crud.create(
		session,
		UserCreate(
			email=_mk_email(),
			role=UserRole.player,
			password="Aaaaaaaa1!",
		),
		is_active=False,
		is_verified=False,
		is_superuser=False,
	)

	u2 = crud.set_role(session, u.id, UserRole.organizer)
	assert u2.role in (getattr(UserRole, "organizer", None), "organizer")

	u3 = crud.set_active_flags(session, u.id, is_active=True, is_verified=True, is_superuser=True)
	assert u3.is_active is True
	assert u3.is_verified is True
	assert u3.is_superuser is True


def test_list_and_delete_users(session: Session):
	u1 = crud.create(
		session,
		UserCreate(email=_mk_email(), role=UserRole.player, password="Aaaaaaaa1!"),
	)
	u2 = crud.create(
		session,
		UserCreate(email=_mk_email(), role=UserRole.player, password="Bbbbbbbb1!"),
	)

	all_users = crud.list_users(session, skip=0, limit=10_000)
	ids = {u.id for u in all_users}
	assert u1.id in ids and u2.id in ids

	ok = crud.delete(session, u1.id)
	assert ok is True
	assert crud.get(session, u1.id) is None

	assert crud.delete(session, u1.id) is False
