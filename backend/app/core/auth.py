from __future__ import annotations

from typing import Generator
from uuid import UUID

from fastapi import Depends
from fastapi_users import FastAPIUsers, BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy
from fastapi_users_db_sqlmodel import SQLModelUserDatabase
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db import get_session
from app.models.user import User

settings = get_settings()


# ── USER DB (sync) ─────────────────────────────────────────────
def get_user_db(session: Session = Depends(get_session), ) -> Generator[SQLModelUserDatabase, None, None]:
	yield SQLModelUserDatabase(session, User)


# ── USER MANAGER (обязателен для FastAPIUsers) ────────────────
class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
	reset_password_token_secret = settings.secret_key
	verification_token_secret = settings.secret_key

	async def on_after_register(self, user: User, request=None):
		return


def get_user_manager(user_db: SQLModelUserDatabase = Depends(get_user_db), ) -> Generator[UserManager, None, None]:
	yield UserManager(user_db)


# ── JWT + Cookie ───────────────────────────────────────────────
def get_jwt_strategy() -> JWTStrategy:
	return JWTStrategy(secret=settings.secret_key, lifetime_seconds=60 * 60 * 24 * 7)  # 7 дней


cookie_transport = CookieTransport(cookie_name="mjwt", cookie_max_age=60 * 60 * 24 * 7, cookie_secure=False,
								   cookie_samesite="lax")

auth_backend = AuthenticationBackend(name="jwt", transport=cookie_transport, get_strategy=get_jwt_strategy, )

fastapi_users = FastAPIUsers[User, UUID](get_user_manager, [auth_backend], )

current_user = fastapi_users.current_user(active=True)
