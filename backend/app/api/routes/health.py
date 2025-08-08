from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["health"])


@router.get("/health", summary="Liveness probe")
def health() -> dict[str, str]:
	return {"status": "ok"}
