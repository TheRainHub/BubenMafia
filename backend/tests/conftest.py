from __future__ import annotations

import os
import pkgutil
import sys
from importlib import import_module
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.compiler import compiles
from sqlmodel import Session, SQLModel, create_engine

# ────────── 1. Fake env для Settings ──────────
os.environ.setdefault(
	"DATABASE_URL",
	"postgresql+psycopg2://user:pass@localhost:5432/test",
)
os.environ.setdefault("SECRET_KEY", "unit-test-secret")

# ────────── 2. PYTHONPATH add <backend> ───────
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

# ────────── 3. Импорт всех моделей ────────────
import app.models as models_pkg  # noqa: E402

for _, mod_name, _ in pkgutil.walk_packages(
		models_pkg.__path__, models_pkg.__name__ + "."
):
	import_module(mod_name)

# ────────── 4. CITEXT → TEXT для SQLite ───────
try:
	from sqlalchemy.dialects.postgresql import CITEXT
except ImportError:  # если пакет не установлен
	CITEXT = None  # type: ignore

if CITEXT is not None:
	@compiles(CITEXT, "sqlite")  # type: ignore[arg-type]
	def _compile_citext_sqlite(element, compiler, **kw):  # noqa: D401
		return "TEXT"

from app.db import get_session  # noqa: E402
# ────────── 5. FastAPI импорт ПОСЛЕ fixes ─────
from app.main import app  # noqa: E402
from app.models.rule import RuleSet  # noqa: E402


# ────────── 6. Engine & Session fixtures ──────
@pytest.fixture(scope="session")
def engine():
	eng = create_engine(
		"sqlite:///:memory:",
		connect_args={"check_same_thread": False},
		echo=False,
	)
	SQLModel.metadata.create_all(eng)

	# ←–– единожды вставляем Default RuleSet(id=1)
	with Session(eng) as seed_sess:
		if not seed_sess.get(RuleSet, 1):
			seed_sess.add(RuleSet(id=1, name="Default", is_active=True))
			seed_sess.commit()

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


# ────────── 8. FastAPI TestClient override ────
@pytest.fixture()
def client(session: Session) -> Generator[TestClient, None, None]:
	app.dependency_overrides[get_session] = lambda: session  # type: ignore[attr-defined]
	try:
		yield TestClient(app)
	finally:
		app.dependency_overrides.clear()  # type: ignore[attr-defined]
