import os
from pathlib import Path
from uuid import UUID

from dotenv import load_dotenv
from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
	JWTStrategy,
	CookieTransport, AuthenticationBackend,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlmodel import Session

from app.db import get_session
from app.models.user import User  # ваша модель

env_path = Path(__file__).parents[2] / ".env"
load_dotenv(env_path)

SECRET = os.environ.get("SECRET_KEY")


def get_user_db(session: Session = Depends(get_session)):
	yield SQLAlchemyUserDatabase(session, User)


def get_jwt_strategy() -> JWTStrategy:
	return JWTStrategy(secret=SECRET, lifetime_seconds=60 * 60 * 24 * 30)  # 30 дней


cookie_transport = CookieTransport(cookie_name="mjwt", cookie_max_age=60 * 60 * 24 * 30)

auth_backend = AuthenticationBackend(
	name="jwt",
	transport=cookie_transport,
	get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, UUID](
	get_user_db,
	[auth_backend],
)

current_user = fastapi_users.current_user(active=True)  # ← нужный символ
