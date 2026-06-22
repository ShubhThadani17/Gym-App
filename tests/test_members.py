def test_create_member_success(client, auth_headers):
    response = client.post("/members", json={
        "name": "Arjun Singh",
        "email": "arjun@gmail.com",
        "phone": "9876543210",
        "age": 22,
        "gender": "Male"
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Arjun Singh"
    assert data["email"] == "arjun@gmail.com"
    assert "id" in data


def test_create_member_requires_auth(client):
    response = client.post("/members", json={
        "name": "Arjun Singh",
        "email": "arjun@gmail.com",
        "phone": "9876543210",
        "age": 22,
        "gender": "Male"
    })
    assert response.status_code == 401


def test_get_member_success(client, auth_headers, sample_member):
    member_id = sample_member["id"]
    response = client.get(f"/members/{member_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == member_id


def test_get_member_not_found(client, auth_headers):
    response = client.get("/members/99999", headers=auth_headers)
    assert response.status_code == 404


def test_get_all_members(client, auth_headers, sample_member):
    response = client.get("/members", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_all_members_empty(client, auth_headers):
    response = client.get("/members", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_update_member(client, auth_headers, sample_member):
    member_id = sample_member["id"]
    response = client.put(f"/members/{member_id}", json={"age": 30}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["age"] == 30
    # Make sure other fields are unchanged
    assert response.json()["name"] == sample_member["name"]


def test_update_member_not_found(client, auth_headers):
    response = client.put("/members/99999", json={"age": 30}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_member_success(client, auth_headers, sample_member):
    member_id = sample_member["id"]
    response = client.delete(f"/members/{member_id}", headers=auth_headers)
    assert response.status_code == 200
    # Verify it is actually gone
    get_response = client.get(f"/members/{member_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_delete_member_not_found(client, auth_headers):
    response = client.delete("/members/99999", headers=auth_headers)
    assert response.status_code == 404


def test_search_member(client, auth_headers, sample_member):
    response = client.get("/members/search?name=Rahul", headers=auth_headers)
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert results[0]["name"] == "Rahul Sharma"


def test_search_member_no_results(client, auth_headers, sample_member):
    response = client.get("/members/search?name=Zzzzzz", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_user_cannot_see_other_users_members(client):
    # Register two different gym owners
    client.post("/auth/register", json={"email": "owner1@test.com", "password": "password123"})
    client.post("/auth/register", json={"email": "owner2@test.com", "password": "password123"})

    token1 = client.post("/auth/login", json={"email": "owner1@test.com", "password": "password123"}).json()["access_token"]
    token2 = client.post("/auth/login", json={"email": "owner2@test.com", "password": "password123"}).json()["access_token"]

    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Owner 1 creates a member
    client.post("/members", json={
        "name": "Private Member",
        "email": "private@gmail.com",
        "phone": "9999999999",
        "age": 28,
        "gender": "Male"
    }, headers=headers1)

    # Owner 2 should see zero members
    response = client.get("/members", headers=headers2)
    assert response.json() == []
