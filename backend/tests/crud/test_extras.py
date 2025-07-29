from uuid import uuid4

from sqlmodel import Session

from app.crud import extras as crud
from app.models.game import Game, GamePlayer
from app.models.player import Player
from app.schemas.extras import ExtraPointsCreate, ExtraPointsUpdate


def _bootstrap_game_with_player(session: Session, rule_set_id: int) -> GamePlayer:
	# минимальный draft‑game с одним слот‑игроком
	g = Game(players_qty=7, rule_set_id=rule_set_id, gm_id=uuid4())
	session.add(g)
	p = Player(nickname="Neo")
	session.add(p)
	session.flush()
	gp = GamePlayer(game_id=g.id, player_id=p.id, seat_no=1, role="Citizen")
	session.add(gp)
	session.commit()
	session.refresh(gp)
	return gp


def test_create_list_update_delete_extras(session: Session, rule_set):
	gp = _bootstrap_game_with_player(session, rule_set.id)

	# CREATE
	e = crud.create(
		session,
		ExtraPointsCreate(game_player_id=gp.id, delta=+0.5, reason="Best speech"),
		user_id=uuid4(),
	)
	assert e.id is not None
	assert e.delta == 0.5

	# LIST by game_id
	lst = crud.list_by_game(session, gp.game_id)
	assert len(lst) == 1 and lst[0].id == e.id

	# UPDATE
	updated = crud.update(session, e.id, ExtraPointsUpdate(delta=-0.3))
	assert updated and updated.delta == -0.3

	# DELETE
	ok = crud.delete(session, e.id)
	assert ok is True
	assert crud.get(session, e.id) is None
