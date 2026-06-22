def test_create_payment_success(client, auth_headers, sample_member):
    response = client.post("/payments", json={
        "member_id": sample_member["id"],
        "amount": 2000.0,
        "payment_method": "upi",
        "status": "paid"
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 2000.0
    assert data["payment_method"] == "upi"


def test_create_payment_invalid_member(client, auth_headers):
    response = client.post("/payments", json={
        "member_id": 99999,
        "amount": 1000.0,
        "payment_method": "cash",
        "status": "paid"
    }, headers=auth_headers)
    assert response.status_code == 404


def test_create_payment_invalid_method(client, auth_headers, sample_member):
    response = client.post("/payments", json={
        "member_id": sample_member["id"],
        "amount": 1000.0,
        "payment_method": "bitcoin",
        "status": "paid"
    }, headers=auth_headers)
    assert response.status_code == 422


def test_create_payment_invalid_status(client, auth_headers, sample_member):
    response = client.post("/payments", json={
        "member_id": sample_member["id"],
        "amount": 1000.0,
        "payment_method": "cash",
        "status": "refunded"
    }, headers=auth_headers)
    assert response.status_code == 422


def test_get_payment(client, auth_headers, sample_payment):
    payment_id = sample_payment["id"]
    response = client.get(f"/payments/{payment_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == payment_id


def test_get_payment_not_found(client, auth_headers):
    response = client.get("/payments/99999", headers=auth_headers)
    assert response.status_code == 404


def test_get_all_payments(client, auth_headers, sample_payment):
    response = client.get("/payments", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_member_payments(client, auth_headers, sample_member, sample_payment):
    member_id = sample_member["id"]
    response = client.get(f"/payments/member/{member_id}", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_total_revenue(client, auth_headers, sample_member):
    # Create two payments and verify total adds up
    client.post("/payments", json={
        "member_id": sample_member["id"],
        "amount": 1000.0,
        "payment_method": "cash",
        "status": "paid"
    }, headers=auth_headers)
    client.post("/payments", json={
        "member_id": sample_member["id"],
        "amount": 500.0,
        "payment_method": "upi",
        "status": "paid"
    }, headers=auth_headers)

    response = client.get("/payments/total-revenue", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total_revenue"] == 1500.0


def test_total_revenue_no_payments(client, auth_headers):
    response = client.get("/payments/total-revenue", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["total_revenue"] == 0
