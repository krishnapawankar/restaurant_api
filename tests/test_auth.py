# tests/test_auth.py
def test_register_and_login(client):
    # Register a new user
    r = client.post("/api/auth/register", json={"username": "kanchan", "password": "kanchanpass"})
    assert r.status_code == 201

    # Login
    r = client.post("/api/auth/login", json={"username": "kanchan", "password": "kanchanpass"})
    assert r.status_code == 200
    assert "access_token" in r.json
