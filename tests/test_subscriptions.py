def test_create_subscription_success(client, auth_headers, sample_member):
    response = client.post("/subscriptions", json={
        "member_id": sample_member["id"],
        "start_date": "2025-01-01",
        "end_date": "2025-02-01",
        "status": "active"
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["member_id"] == sample_member["id"]
    assert data["status"] == "active"


def test_create_subscription_invalid_member(client, auth_headers):
    response = client.post("/subscriptions", json={
        "member_id": 99999,
        "start_date": "2025-01-01",
        "end_date": "2025-02-01",
        "status": "active"
    }, headers=auth_headers)
    assert response.status_code == 404


def test_create_subscription_invalid_status(client, auth_headers, sample_member):
    # Pydantic Literal should reject anything not in the allowed list
    response = client.post("/subscriptions", json={
        "member_id": sample_member["id"],
        "start_date": "2025-01-01",
        "end_date": "2025-02-01",
        "status": "banana"
    }, headers=auth_headers)
    assert response.status_code == 422


def test_get_subscription(client, auth_headers, sample_subscription):
    sub_id = sample_subscription["id"]
    response = client.get(f"/subscriptions/{sub_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == sub_id


def test_get_subscription_not_found(client, auth_headers):
    response = client.get("/subscriptions/99999", headers=auth_headers)
    assert response.status_code == 404


def test_get_all_subscriptions(client, auth_headers, sample_subscription):
    response = client.get("/subscriptions", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_renew_subscription(client, auth_headers, sample_subscription):
    sub_id = sample_subscription["id"]
    response = client.post(f"/subscriptions/{sub_id}/renew", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    # end_date should have moved forward by 30 days
    from datetime import date, timedelta
    original_end = date.fromisoformat(sample_subscription["end_date"])
    new_end = date.fromisoformat(data["end_date"])
    assert new_end > original_end


def test_renew_subscription_not_found(client, auth_headers):
    response = client.post("/subscriptions/99999/renew", headers=auth_headers)
    assert response.status_code == 404


def test_cancel_subscription(client, auth_headers, sample_subscription):
    sub_id = sample_subscription["id"]
    response = client.post(f"/subscriptions/{sub_id}/cancel", headers=auth_headers)
    assert response.status_code == 200


def test_cancel_subscription_not_found(client, auth_headers):
    response = client.post("/subscriptions/99999/cancel", headers=auth_headers)
    assert response.status_code == 404
