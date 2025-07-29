from __future__ import annotations

import re
import uuid
from typing import Tuple

import pytest
from httpx import Response
from sqlmodel import Session, select

from app.models.user import User

COOKIE_NAME = "mjwt"  # Имя cookie — должно совпадать с вашим CookieTransport


# ---------- ВСПОМОГАТЕЛЬНЫЕ УТИЛИТЫ ----------

def rand_email(prefix: str = "user") -> str:
	"""Генерирует уникальный email, чтобы тесты не конфликтовали друг с другом."""
	return f"{prefix}-{uuid.uuid4().hex[:8]}@example.com"


def register(
		client,
		*,
		email: str,
		password: str = "StrongPass123!",
		role: str = "gm",
		expect_status: Tuple[int, ...] = (200, 201),
) -> Response:
	r = client.post("/auth/register", json={"email": email, "password": password, "role": role})
	assert r.status_code in expect_status, f"Unexpected register status {r.status_code}: {r.text}"
	return r


def login_cookie(
		client,
		*,
		email: str,
		password: str,
		expect_status: Tuple[int, ...] = (204,),
		form_content_type: bool = True,
) -> Response:
	if form_content_type:
		r = client.post(
			"/auth/jwt/login",
			data={"username": email, "password": password},
			headers={"Content-Type": "application/x-www-form-urlencoded"},
		)
	else:
		# Намеренно неверный формат — JSON
		r = client.post("/auth/jwt/login", json={"username": email, "password": password})
	assert r.status_code in expect_status, f"Unexpected login status {r.status_code}: {r.text}"
	return r


def logout(client, expect_status: Tuple[int, ...] = (204,)) -> Response:
	r = client.post("/auth/jwt/logout")
	assert r.status_code in expect_status, f"Unexpected logout status {r.status_code}: {r.text}"
	return r


def get_me(client, expect_status: Tuple[int, ...] = (200,)) -> Response:
	r = client.get("/users/me")
	assert r.status_code in expect_status, f"Unexpected /users/me status {r.status_code}: {r.text}"
	return r


# ---------- ТЕСТЫ ОСНОВНОГО ПОТОКА С ДОП. ПРОВЕРКАМИ ----------

def test_full_cookie_flow_and_headers(client):
	email = rand_email("gm")
	register(client, email=email, role="gm")

	# Логин и проверка установки cookie
	r = login_cookie(client, email=email, password="StrongPass123!")
	assert COOKIE_NAME in client.cookies, "JWT cookie not set"

	# Дополнительно проверим заголовок Set-Cookie на HttpOnly
	set_cookie = "; ".join(r.headers.get_list("set-cookie"))
	assert COOKIE_NAME in set_cookie
	assert "HttpOnly" in set_cookie or "httponly" in set_cookie.lower()

	# Доступ к защищённому эндпоинту
	r = get_me(client)
	me = r.json()
	assert me["email"].lower() == email.lower()
	assert me.get("role") == "gm"

	# Логаут и удаление cookie
	r = logout(client)
	set_cookie_logout = "; ".join(r.headers.get_list("set-cookie"))
	# Обычно удаление — это Set-Cookie: mjwt=; Max-Age=0 ...
	assert COOKIE_NAME in set_cookie_logout
	assert ("Max-Age=0" in set_cookie_logout) or re.search(r"Expires=.+", set_cookie_logout)
	# И больше доступ без авторизации быть не должен
	get_me(client, expect_status=(401, 403))


# ---------- РЕГИСТРАЦИЯ: ВАЛИДАЦИЯ И ДУБЛИКАТЫ ----------

@pytest.mark.parametrize(
	"payload,expected",
	[
		({"password": "StrongPass123!", "role": "gm"}, (422,)),  # нет email
		({"email": "no-at-sign", "password": "StrongPass123!", "role": "gm"}, (422,)),  # невалидный email
		({"email": "x@example.com", "role": "gm"}, (422,)),  # нет password
		({"email": "x@example.com", "password": "StrongPass123!", "role": "unknown"}, (422,)),  # несуществующая роль
	],
)
def test_register_invalid_payloads(client, payload, expected):
	r = client.post("/auth/register", json=payload)
	assert r.status_code in expected, f"Unexpected status {r.status_code}: {r.text}"


def test_register_duplicate_email_case_insensitive(client):
	email = rand_email("dup")
	register(client, email=email, role="gm")
	# Повтор другой раскладкой
	email_upper = email.upper()
	r = client.post("/auth/register", json={"email": email_upper, "password": "StrongPass123!", "role": "gm"})
	# В зависимости от реализации это может быть 400 или 409 (или 422).
	assert r.status_code in (400, 409, 422), f"Expected duplicate rejection, got {r.status_code}: {r.text}"


def test_register_different_roles_and_me(client):
	# Если в вашей Enum есть 'player' — проверим, что она сохраняется.
	email = rand_email("player")
	r = client.post("/auth/register", json={"email": email, "password": "StrongPass123!", "role": "player"})
	assert r.status_code in (200, 201), r.text
	login_cookie(client, email=email, password="StrongPass123!")
	me = get_me(client).json()
	assert me.get("role") == "player"


# ---------- ЛОГИН: НЕВЕРНЫЕ ДАННЫЕ И ФОРМАТЫ ----------

@pytest.mark.parametrize(
	"email,password,expected",
	[
		("nouser@example.com", "whatever", (400, 401)),  # несуществующий пользователь
		# Сначала зарегистрируем, потом неверный пароль
	],
)
def test_login_invalid_credentials_unknown_user(client, email, password, expected):
	r = login_cookie(client, email=email, password=password, expect_status=expected)
	# cookie не должно быть
	assert COOKIE_NAME not in client.cookies


def test_login_invalid_credentials_wrong_password(client):
	email = rand_email("wrongpass")
	register(client, email=email)
	r = login_cookie(client, email=email, password="WRONG", expect_status=(400, 401))
	assert COOKIE_NAME not in client.cookies


def test_login_requires_form_urlencoded(client):
	email = rand_email("form")
	register(client, email=email)
	# Неверный тип данных — JSON
	login_cookie(client, email=email, password="StrongPass123!", expect_status=(415, 422, 405), form_content_type=False)


# ---------- ДОСТУП К /users/me ПРИ РАЗНЫХ УСЛОВИЯХ ----------

def test_me_unauthorized_without_cookie(client):
	r = client.get("/users/me")
	assert r.status_code in (401, 403), r.text


def test_me_with_tampered_cookie(client):
	email = rand_email("tamper")
	register(client, email=email)
	login_cookie(client, email=email, password="StrongPass123!")
	assert COOKIE_NAME in client.cookies

	# Портим токен одним символом
	bad = client.cookies.get(COOKIE_NAME)[:-1] + "x"
	client.cookies.set(COOKIE_NAME, bad)

	get_me(client, expect_status=(401, 403))


def test_logout_idempotent(client):
	email = rand_email("twice")
	register(client, email=email)
	login_cookie(client, email=email, password="StrongPass123!")
	logout(client, expect_status=(204,))
	# Повторный логаут: в разных реализациях может быть 204 (идемпотентно) или 401/403
	r = logout(client, expect_status=(204, 401, 403))


# не должно падать исключение по assert


# ---------- ПОВЕДЕНИЕ ДЛЯ НЕАКТИВНОГО ПОЛЬЗОВАТЕЛЯ ----------

@pytest.mark.skipif(User is None, reason="Не найден импорт модели User; скорректируйте путь импорта.")
def test_inactive_user_cannot_login(client, session: Session):
	"""
	Создаём пользователя, помечаем is_active=False и убеждаемся, что аутентификация запрещена.
	В FastAPI Users это может возвращать 400/401/403 — даём люфт.
	"""
	email = rand_email("inactive")
	register(client, email=email)
	user = session.exec(select(User).where(User.email == email)).first()
	assert user is not None, "User not found after registration"
	user.is_active = False
	session.add(user)
	session.commit()

	# Попытка логина должна быть отклонена
	r = login_cookie(client, email=email, password="StrongPass123!", expect_status=(400, 401, 403))
	assert COOKIE_NAME not in client.cookies
