def test_register_login_me_logout(client):
	payload = {"email": "gm@example.com", "password": "StrongPass123!", "role": "gm"}

	# Регистрация
	r = client.post("/api/auth/register", json=payload)
	assert r.status_code in (200, 201), r.text

	# Логин (Cookie)
	r = client.post(
		"/api/auth/jwt/login",
		data={"username": "gm@example.com", "password": "StrongPass123!"},
		headers={"Content-Type": "application/x-www-form-urlencoded"},
	)
	assert r.status_code == 204, r.text
	# Проверяем, что cookie проставлен
	assert "mjwt" in client.cookies

	# Защищённый эндпоинт
	r = client.get("/api/users/me")
	assert r.status_code == 200
	me = r.json()
	assert me["email"] == "gm@example.com"
	assert me["role"] == "gm"

	# Логаут
	r = client.post("/api/auth/jwt/logout")
	assert r.status_code == 204

	# После логаута доступ закрыт
	r = client.get("/api/users/me")
	assert r.status_code in (401, 403)
