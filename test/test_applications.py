from fastapi.testclient import TestClient
from app.main import app
import pytest


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

def test_patch_application_company():
    response = client.patch(
        "/applications/5",
        json ={
            "company": "Microsoft",
        },
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Microsoft"
    assert response.json()["position"] == "Backend"
    assert response.json()["status"] == "applied"

def test_get_application():
    response = client.get("/applications/5")

    assert response.status_code == 200
    assert response.json()["id"] == 5
    assert response.json()["company"] == "Microsoft"
    assert response.json()["position"] == "Backend"
    assert response.json()["status"] == "applied"

def test_get_application_not_found():
    response = client.get("/applications/999999")

    assert response.status_code == 404

def test_delete_application():
    response = client.delete("/applications/5")

    assert response.status_code == 200