import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "testsecretkey12345678901234567890"
os.environ["ALGORITHM"] = "HS256"
os.environ["TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["EMAIL_ADDRESS"] = "test@test.com"
os.environ["EMAIL_PASSWORD"] = "testpassword"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from database.db import get_db
from main import app

# Use an in-memory SQLite database for tests — no Postgres needed
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# This replaces the real DB with the test DB before any test runs
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    # Fresh tables before every single test — complete isolation
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    """Creates a user and returns their credentials."""
    client.post("/auth/register", json={
        "email": "gym@test.com",
        "password": "password123"
    })
    return {"email": "gym@test.com", "password": "password123"}


@pytest.fixture
def auth_headers(client, registered_user):
    """Logs in and returns the Authorization header dict."""
    response = client.post("/auth/login", json=registered_user)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_member(client, auth_headers):
    """Creates a member and returns the full response JSON."""
    response = client.post("/members", json={
        "name": "Rahul Sharma",
        "email": "rahul@gmail.com",
        "phone": "9876543210",
        "age": 25,
        "gender": "Male"
    }, headers=auth_headers)
    return response.json()


@pytest.fixture
def sample_subscription(client, auth_headers, sample_member):
    """Creates a subscription for the sample member."""
    response = client.post("/subscriptions", json={
        "member_id": sample_member["id"],
        "start_date": "2025-01-01",
        "end_date": "2025-02-01",
        "status": "active"
    }, headers=auth_headers)
    return response.json()


@pytest.fixture
def sample_payment(client, auth_headers, sample_member):
    """Creates a payment for the sample member."""
    response = client.post("/payments", json={
        "member_id": sample_member["id"],
        "amount": 1500.0,
        "payment_method": "upi",
        "status": "paid"
    }, headers=auth_headers)
    return response.json()
