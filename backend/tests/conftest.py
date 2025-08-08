from __future__ import annotations

import os
import pkgutil
import sys
from importlib import import_module
from pathlib import Path
from typing import Generator, Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

# ────────── 1. Fake env для Settings ──────────
os.environ.setdefault(
	"DATABASE_URL",
	"postgresql+psycopg2://user:pass@localhost:5432/test",
)
os.environ.setdefault("SECRET_KEY", "unit-test-secret")
os.environ.setdefault("TESTING", "1")

# ────────── 2. PYTHONPATH add <backend> ───────
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

# ────────── 3. Импорт всех моделей ────────────
import app.models as models_pkg  # noqa: E402

for _, mod_name, _ in pkgutil.walk_packages(models_pkg.__path__, models_pkg.__name__ + "."):
	import_module(mod_name)

# ────────── 4. CITEXT → TEXT для SQLite ───────
try:
	from sqlalchemy.dialects.postgresql import CITEXT
except ImportError:  # если пакет не установлен
	CITEXT = None  # type: ignore

if CITEXT is not None:
	@compiles(CITEXT, "sqlite")  # type: ignore[arg-type]
	def _compile_citext_sqlite(element, compiler, **kw):  # noqa: D401
		return "TEXT COLLATE NOCASE"

from app.db import get_session  # noqa: E402
# ────────── 5. FastAPI импорт ПОСЛЕ fixes ─────
from app.main import create_app  # noqa: E402
from app.models.rule import RuleSet  # noqa: E402


# ────────── 6. Engine & Session fixtures ──────
@pytest.fixture(scope="session")
def engine():
	eng = create_engine(
		"sqlite+pysqlite:///:memory:",
		connect_args={"check_same_thread": False},
		poolclass=StaticPool,
		# ← один коннект на все потоки и сессии
		echo=False,
	)
	SQLModel.metadata.create_all(eng)

	# Сид "дефолтного" RuleSet(id=1) один раз на всю сессию pytest
	from app.models.rule import RuleSet

	with Session(eng) as seed:
		if not seed.get(RuleSet, 1):
			seed.add(RuleSet(id=1, name="Default", is_active=True))
			seed.commit()

	return eng


@pytest.fixture()
def session(engine) -> Generator[Session, None, None]:
	with Session(engine) as sess:
		yield sess
		sess.rollback()  # «чистая» транзакция для каждого теста


# ────────── 7. rule_set fixture (без insert) ───
@pytest.fixture()
def rule_set(session: Session) -> RuleSet:
	return session.get(RuleSet, 1)  # type: ignore[return-value]


@pytest.fixture()
def client(engine) -> Iterator[TestClient]:
	# Явно типизируем зависимость как генератор сессии
	def override_get_session() -> Iterator[Session]:
		with Session(engine) as s:
			yield s

	app = create_app()
	app.dependency_overrides[get_session] = override_get_session  # type: ignore[attr-defined]
	try:
		with TestClient(app) as c:
			yield c
	finally:
		app.dependency_overrides.clear()  # type: ignore[attr-defined]
