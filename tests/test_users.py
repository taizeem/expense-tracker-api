from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "newuser"
    assert "password" not in data
    assert "password_hash" not in data

def test_create_duplicate_user():
    client.post(
        "/users/",
        json={
            "username": "duplicateuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/users/",
        json={
            "username": "duplicateuser",
            "password": "password123"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"
