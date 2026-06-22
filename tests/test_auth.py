def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "user@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User registered , Please Login"


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "user@test.com", "password": "password123"})
    response = client.post("/auth/register", json={"email": "user@test.com", "password": "password123"})
    assert response.status_code == 400
    assert "Email Already Exists" in response.json()["detail"]


def test_login_success(client):
    client.post("/auth/register", json={"email": "user@test.com", "password": "password123"})
    response = client.post("/auth/login", json={"email": "user@test.com", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "user@test.com", "password": "password123"})
    response = client.post("/auth/login", json={"email": "user@test.com", "password": "wrongpassword"})
    assert response.status_code == 401


def test_login_nonexistent_email(client):
    response = client.post("/auth/login", json={"email": "nobody@test.com", "password": "password123"})
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/members")
    assert response.status_code == 401


def test_protected_route_with_invalid_token(client):
    response = client.get("/members", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 401
