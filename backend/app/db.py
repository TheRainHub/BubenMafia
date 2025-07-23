from typing import AsyncGenerator, Generator

from app.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

settings = get_settings()

sync_engine = create_engine(settings.sync_dsn, pool_pre_ping=True)
async_engine = create_async_engine(settings.async_dsn, pool_pre_ping=True, future=True)

sync_session_maker = sessionmaker(sync_engine, class_=Session, expire_on_commit=False)
async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


def get_session() -> Generator[Session, None, None]:
    with sync_session_maker() as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
