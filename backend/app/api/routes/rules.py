from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.deps import get_db, current_organizer  # аналог current_gm
from app.crud import rules as crud
from app.schemas.rules import (
	RuleSetCreate,
	RuleSetRead,
	RuleSetUpdate,
	RuleItemCreate,
	RuleItemRead,
	RuleItemUpdate,
)

router = APIRouter(prefix="/rulesets", tags=["rulesets"], dependencies=[Depends(current_organizer)])


# ─────────── RULE SETS ───────────
@router.post("/", response_model=RuleSetRead, status_code=status.HTTP_201_CREATED)
def create_ruleset(payload: RuleSetCreate, session: Session = Depends(get_db)):
	return crud.create_ruleset(session, payload)


@router.get("/", response_model=list[RuleSetRead])
def list_rulesets(session: Session = Depends(get_db)):
	return crud.list_rulesets(session)


@router.get("/{rs_id}", response_model=RuleSetRead)
def get_ruleset(rs_id: int, session: Session = Depends(get_db)):
	rs = crud.get_ruleset(session, rs_id)
	if not rs:
		raise HTTPException(404, "RuleSet not found")
	return rs


@router.patch("/{rs_id}", response_model=RuleSetRead)
def update_ruleset(
		rs_id: int, payload: RuleSetUpdate, session: Session = Depends(get_db)
):
	rs = crud.update_ruleset(session, rs_id, payload)
	if not rs:
		raise HTTPException(404, "RuleSet not found")
	return rs


@router.delete("/{rs_id}", status_code=204)
def delete_ruleset(rs_id: int, session: Session = Depends(get_db)):
	ok = crud.delete_ruleset(session, rs_id)
	if not ok:
		raise HTTPException(404, "RuleSet not found")


# ─────────── RULE ITEMS ───────────
@router.post(
	"/{rs_id}/items/",
	response_model=RuleItemRead,
	status_code=status.HTTP_201_CREATED,
)
def create_item(
		rs_id: int, payload: RuleItemCreate, session: Session = Depends(get_db)
):
	return crud.create_item(session, rs_id, payload)


@router.patch("/items/{item_id}", response_model=RuleItemRead)
def update_item(
		item_id: int, payload: RuleItemUpdate, session: Session = Depends(get_db)
):
	item = crud.update_item(session, item_id, payload)
	if not item:
		raise HTTPException(404, "RuleItem not found")
	return item


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, session: Session = Depends(get_db)):
	ok = crud.delete_item(session, item_id)
	if not ok:
		raise HTTPException(404, "RuleItem not found")
