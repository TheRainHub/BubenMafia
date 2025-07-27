import datetime as dt
import uuid
from typing import Sequence, cast

from sqlmodel import Session

from app.core.enums import GameRole, GameState
from app.crud import games as crud
from app.models.game import GamePlayer
from app.models.player import Player
from app.schemas.games import GameCreate


# ────────────── helpers ─────────────────────────────────
def _sample_game(session: Session, rule_set_id: int):
	data = GameCreate(players_qty=9, rule_set_id=rule_set_id)
	gm_id = uuid.uuid4()
	return crud.create(session, data, gm_id)


# ────────────── tests ───────────────────────────────────
def test_create_and_get(session: Session, rule_set):
	g = _sample_game(session, rule_set.id)

	assert g.id is not None
	assert g.state == GameState.draft

	fetched = crud.get(session, g.id)
	assert fetched and fetched.id == g.id
	assert fetched.players_qty == 9


def test_get_with_players(session: Session, rule_set):
	g = _sample_game(session, rule_set.id)

	# add player + link
	p = Player(nickname="Tester")
	session.add(p)
	session.commit()

	gp = GamePlayer(
		game_id=g.id,
		player_id=p.id,
		seat_no=1,
		role=GameRole.citizen,
	)
	session.add(gp)
	session.commit()

	fetched = crud.get(session, g.id, with_players=True)
	assert fetched

	players = cast(Sequence[GamePlayer], fetched.players)
	assert len(players) == 1
	assert players[0].seat_no == 1


def test_list_ordering(session: Session, rule_set):
	g1 = _sample_game(session, rule_set.id)
	g2 = _sample_game(session, rule_set.id)

	lst = crud.list_games(session, skip=0, limit=10)
	assert lst[0].id == g2.id and lst[1].id == g1.id


def test_update_state(session: Session, rule_set):
	g = _sample_game(session, rule_set.id)

	aware_now = dt.datetime.now(dt.UTC)
	finished_at = aware_now.replace(tzinfo=None)

	updated = crud.update_state(
		session, g.id, GameState.finished, finished_at=finished_at
	)

	assert updated and updated.state == GameState.finished
	assert updated.finished_at == finished_at


def test_delete(session: Session, rule_set):
	g = _sample_game(session, rule_set.id)
	assert crud.delete(session, g.id)
	assert crud.get(session, g.id) is None


def test_delete_missing(session: Session):
	assert not crud.delete(session, 9999)
