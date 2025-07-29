from sqlmodel import Session

from app.crud import rules as crud
from app.schemas.rules import RuleSetCreate, RuleItemCreate


def test_create_ruleset(session: Session):
	payload = RuleSetCreate(
		name="Test",
		is_active=True,
		items=[RuleItemCreate(condition="CITY_WIN", role_filter="Citizen", delta=3.0)]
	)
	rs = crud.create_ruleset(session, payload)
	assert rs.id
	assert rs.items[0].condition == "CITY_WIN"


def test_unique_active_ruleset(session: Session):
	crud.create_ruleset(session, RuleSetCreate(name="R1", is_active=True))
	crud.create_ruleset(session, RuleSetCreate(name="R2", is_active=True))
	active = [r for r in crud.list_rulesets(session) if r.is_active]
	assert len(active) == 1
