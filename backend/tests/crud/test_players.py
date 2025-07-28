import pytest
from sqlmodel import Session

from app.crud import players as crud
from app.schemas.players import PlayerCreate


def test_create_and_get(session: Session):
    p = crud.create(session, PlayerCreate(nickname="Leo"))
    assert p.id is not None
    fetched = crud.get(session, p.id)
    assert fetched.nickname == "Leo"


def test_unique_nickname(session: Session):
    crud.create(session, PlayerCreate(nickname="Mila"))
    crud.create(session, PlayerCreate(nickname="Richard"))
    with pytest.raises(ValueError):
        crud.create(session, PlayerCreate(nickname="mila"))  # CITEXT => case‑insensitive
    crud.create(session, PlayerCreate(nickname="Anya"))
    crud.create(session, PlayerCreate(nickname="Selenix"))
    with pytest.raises(ValueError):
        crud.create(session, PlayerCreate(nickname="Richard"))
    with pytest.raises(ValueError):
        crud.create(session, PlayerCreate(nickname="Mila"))
