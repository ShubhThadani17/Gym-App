def test_dashboard_empty(client, auth_headers):
    response = client.get("/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_members"] == 0
    assert data["active_subscriptions"] == 0
    assert data["expired_subscriptions"] == 0
    assert data["total_revenue"] == 0


def test_dashboard_with_data(client, auth_headers, sample_member, sample_subscription, sample_payment):
    response = client.get("/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_members"] == 1
    assert data["active_subscriptions"] == 1
    assert data["total_revenue"] == sample_payment["amount"]


def test_dashboard_requires_auth(client):
    response = client.get("/dashboard")
    assert response.status_code == 401


def test_dashboard_counts_only_own_data(client):
    # Two owners, each with their own member
    client.post("/auth/register", json={"email": "owner1@test.com", "password": "password123"})
    client.post("/auth/register", json={"email": "owner2@test.com", "password": "password123"})

    token1 = client.post("/auth/login", json={"email": "owner1@test.com", "password": "password123"}).json()["access_token"]
    token2 = client.post("/auth/login", json={"email": "owner2@test.com", "password": "password123"}).json()["access_token"]

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    client.post("/members", json={
        "name": "Member One",
        "email": "m1@gmail.com",
        "phone": "9111111111",
        "age": 25,
        "gender": "Male"
    }, headers=headers1)

    # Owner 2's dashboard should show 0, not 1
    response = client.get("/dashboard", headers=headers2)
    assert response.json()["total_members"] == 0
