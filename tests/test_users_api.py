VALID_BODY = {
    "username": "alex",
    "email": "alex@example.org",
    "role": "worker",
    "password": "StrongP@ss",
}


def test_create_user_success(client, monkeypatch):
    # Fake service to return a shape matching UserCreateRes
    async def fake_register_user(req):
        # req is a UserCreateReq (has username/email/role/password)
        return {
            "id": "u_123",
            "username": req.username,
            "email": req.email,
            "role": req.role,
            "meta": {"created": True},
        }

    monkeypatch.setattr("app.api.v1.users.register_user", fake_register_user)

    resp = client.post("/users", json=VALID_BODY)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["id"] == "u_123"
    assert data["username"] == VALID_BODY["username"]
    assert data["email"] == VALID_BODY["email"]
    assert data["role"] == VALID_BODY["role"]
    assert "meta" in data
