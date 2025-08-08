from __future__ import annotations

from fastapi import APIRouter

api_router = APIRouter(prefix="/api")


def _optional_include(router: APIRouter, module_path: str, *, attr: str = "router") -> None:
	"""
	Пытается импортировать модуль и подключить его router.
	Если модуля нет или нет атрибута router — просто пропускаем.
	"""
	try:
		mod = __import__(module_path, fromlist=[attr])
		subrouter = getattr(mod, attr, None)
		if subrouter is not None:
			router.include_router(subrouter)
	except Exception:
		# Ничего не делаем — модуль пока не реализован / не подключён
		pass


_optional_include(api_router, "app.api.routes.health")  # /health
_optional_include(api_router, "app.api.routes.users")  # /users
_optional_include(api_router, "app.api.routes.auth")  # /auth
_optional_include(api_router, "app.api.routes.players")  # /players
_optional_include(api_router, "app.api.routes.extras")  # /extras
_optional_include(api_router, "app.api.routes.rules")  # /rules
_optional_include(api_router, "app.api.routes.games")  # /games
_optional_include(api_router, "app.api.routes.stats")  # /stats
