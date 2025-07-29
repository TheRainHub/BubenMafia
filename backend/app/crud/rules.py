from __future__ import annotations

from typing import Sequence, Optional

from sqlmodel import Session, select, update

from app.models.rule import RuleSet, RuleItem
from app.schemas.rules import (RuleSetCreate, RuleSetUpdate, RuleItemCreate, RuleItemUpdate, )


# ────────── RULE SETS ──────────
def create_ruleset(session: Session, data: RuleSetCreate) -> RuleSet:
	rs = RuleSet(name=data.name, is_active=data.is_active)
	session.add(rs)
	session.flush()  # получаем rs.id
	if data.is_active:
		session.exec(
			update(RuleSet)
			.where(
				RuleSet.id != rs.id,
				RuleSet.is_active == True  # ✅ вариант 1 (проще)
				# RuleSet.is_active.is_(true())    # ✅ вариант 2
			)
			.values(is_active=False)
		)

	# child items
	for item in data.items:
		session.add(
			RuleItem(rule_set_id=rs.id, condition=item.condition, role_filter=item.role_filter, delta=item.delta))

	session.commit()
	session.refresh(rs)
	return rs


def get_ruleset(session: Session, ruleset_id: int) -> Optional[RuleSet]:
	return session.get(RuleSet, ruleset_id)


def list_rulesets(session: Session) -> Sequence[RuleSet]:
	stmt = select(RuleSet).order_by(RuleSet.id)
	return session.exec(stmt).all()


def update_ruleset(session: Session, ruleset_id: int, data: RuleSetUpdate) -> Optional[RuleSet]:
	rs = session.get(RuleSet, ruleset_id)
	if not rs:
		return None
	for k, v in data.model_dump(exclude_unset=True).items():
		setattr(rs, k, v)

	# если сделали активным – остальные деактивируем
	if data.is_active:
		session.exec(
			update(RuleSet)
			.where(RuleSet.id != rs.id, RuleSet.is_active == True)
			.values(is_active=False)
		)
	session.commit()
	session.refresh(rs)
	return rs


def delete_ruleset(session: Session, ruleset_id: int) -> bool:
	rs = session.get(RuleSet, ruleset_id)
	if not rs:
		return False
	session.delete(rs)
	session.commit()
	return True


# ────────── RULE ITEMS ──────────
def create_item(session: Session, ruleset_id: int, data: RuleItemCreate) -> RuleItem:
	obj = RuleItem(rule_set_id=ruleset_id, condition=data.condition, role_filter=data.role_filter, delta=data.delta, )
	session.add(obj)
	session.commit()
	session.refresh(obj)
	return obj


def update_item(session: Session, item_id: int, data: RuleItemUpdate) -> Optional[RuleItem]:
	obj = session.get(RuleItem, item_id)
	if not obj:
		return None
	for k, v in data.model_dump(exclude_unset=True).items():
		setattr(obj, k, v)
	session.commit()
	session.refresh(obj)
	return obj


def delete_item(session: Session, item_id: int) -> bool:
	obj = session.get(RuleItem, item_id)
	if not obj:
		return False
	session.delete(obj)
	session.commit()
	return True
