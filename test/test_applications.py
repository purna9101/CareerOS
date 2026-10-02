from fastapi.testclient import TestClient
from app.main import app
from app.main import get_db
import pytest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)



@pytest.fixture
def application():
    response = client.post(
        "/applications",
        json ={
            "company": "Test Company",
            "position": "Test Developer",
            "status": "applied",
        },
    )

    return response.json()

def test_fixture_application(application):
    assert application["company"] == "Test Company"
    assert application["position"] == "Test Developer"
    assert application["status"] == "applied"


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
            "status": "applied",
        },
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Google"
    assert response.json()["position"] == "Backend Developer"
    assert response.json()["status"] == "applied"

def test_create_application_invalid_status():
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
            "status": "banana",
        },
    )

    assert response.status_code == 422 

def test_create_application_blank_company():
    response = client.post(
        "/applications",
        json={
            "company": "   ",
            "position": "Backend Developer",
            "status": "applied",
        },
    )

    assert response.status_code == 422

def test_create_application_company_too_long():
    response = client.post(
        "/applications",
        json={
            "company": "A" * 256,
            "position": "Backend Developer",
            "status": "applied",
        },
    )

    assert response.status_code == 422 

def test_patch_application_company_too_long():
    response = client.patch(
        "/applications/5",
        json = {
            "company": "A" * 256,
        }
    )

    assert response.status_code == 422

def test_patch_application_company(application):
    application_id = application["id"]

    response = client.patch(
        f"/applications/{application_id}",
        json={
            "company": "Microsoft",
        },
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Microsoft"
    assert response.json()["position"] == "Test Developer"
    assert response.json()["status"] == "applied"


def test_get_application(application):
    application_id = application["id"]
    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json()["id"] == application_id
    assert response.json()["company"] == "Test Company"
    assert response.json()["position"] == "Test Developer"
    assert response.json()["status"] == "applied"

def test_get_application_not_found():
    response = client.get("/applications/999999")

    assert response.status_code == 404

def test_delete_application(application):
    application_id = application["id"]
    response = client.delete(f"/applications/{application_id}")

    assert response.status_code == 200

    response = client.get(
        f"/applications/{application_id}"
    )

    assert response.status_code == 404
    