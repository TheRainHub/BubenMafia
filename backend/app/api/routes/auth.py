from __future__ import annotations

from fastapi import APIRouter

# подстрой пути импорта под свой проект
from app.core.auth import auth_backend, fastapi_users
from app.schemas.users import UserCreate, UserRead, UserUpdate

router = APIRouter()

# JWT login/logout (и refresh, если настроен)
router.include_router(
	fastapi_users.get_auth_router(auth_backend),
	prefix="/auth/jwt",
	tags=["auth"],
)

# регистрация (self-signup)
router.include_router(
	fastapi_users.get_register_router(UserRead, UserCreate),
	prefix="/auth",
	tags=["auth"],
)

# CRUD пользователей от fastapi-users (GET/PUT текущего и админские операции — зависит от конфигурации)
router.include_router(
	fastapi_users.get_users_router(UserRead, UserUpdate),
	prefix="/users",
	tags=["users"],
)
