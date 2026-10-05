from fastapi.testclient import TestClient
from app.main import app
from app.main import global_exception_handler
from app.main import get_db
import pytest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(bind=test_engine)

@pytest.fixture
def db_connection():
    connection = test_engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_connection):
    def override_get_db():
        db = TestSessionLocal(bind=db_connection)
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(
        app,
        raise_server_exceptions=False,
        )

    app.dependency_overrides.clear()


@pytest.fixture
def application(client):
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


def test_create_application(client):
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

def test_create_application_invalid_status(client):
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
            "status": "banana",
        },
    )

    assert response.status_code == 422 

def test_create_application_blank_company(client):
    response = client.post(
        "/applications",
        json={
            "company": "   ",
            "position": "Backend Developer",
            "status": "applied",
        },
    )

    assert response.status_code == 422

def test_create_application_company_too_long(client):
    response = client.post(
        "/applications",
        json={
            "company": "A" * 256,
            "position": "Backend Developer",
            "status": "applied",
        },
    )

    assert response.status_code == 422 

def test_patch_application_company_too_long(client, application):
    application_id = application["id"]

    response = client.patch(
        f"/applications/{application_id}",
        json={
            "company": "A" * 256,
        },
    )

    assert response.status_code == 422

def test_patch_application_company(client,application):
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


def test_get_application(client,application):
    application_id = application["id"]
    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json()["id"] == application_id
    assert response.json()["company"] == "Test Company"
    assert response.json()["position"] == "Test Developer"
    assert response.json()["status"] == "applied"

def test_get_application_not_found(client):
    response = client.get("/applications/999999")

    assert response.status_code == 404

def test_delete_application(client,application):
    application_id = application["id"]
    response = client.delete(f"/applications/{application_id}")

    assert response.status_code == 200

    response = client.get(
        f"/applications/{application_id}"
    )

    assert response.status_code == 404



@pytest.mark.anyio
async def test_global_exception_handler():
    response = await global_exception_handler(
        None,
        RuntimeError("test error"),
    )

    assert response.status_code == 500
    assert response.body == b'{"detail":"Internal server error"}'