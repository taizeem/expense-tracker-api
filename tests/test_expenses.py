from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_expenses():
    response = client.get("/expenses/")

    assert response.status_code == 200

def test_create_expense():
    response = client.post(
        "/expenses",
        json={
            "title": "Test Lunch",
            "amount": 200,
            "category": "food"
        }
    )
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Test Lunch"
    assert data["amount"] == 200
    assert data["category"] == "food"


def test_get_expense():
    response = client.post(
        "/expenses/",
        json={
            "title":"Test Dinner",
            "amount":200,
            "category":"food"
        }
    )
    expense_id = response.json()["id"]

    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code==200

    data = response.json()
    assert data["id"] == expense_id
    assert data["title"] == "Test Dinner"

def test_get_expense_not_found():
    response = client.get("/expenses/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_update_expense():
    create_response = client.post(
        "/expenses/",
        json={
            "title": "Old Title",
            "amount": 100,
            "category": "food"
        }
    )

    expense_id = create_response.json()["id"]

    update_response = client.put(
        f"/expenses/{expense_id}",
        json={
            "title": "New Title",
            "amount": 500,
            "category": "shopping"
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == expense_id
    assert data["title"] == "New Title"
    assert data["amount"] == 500
    assert data["category"] == "shopping"

def test_delete_expense():
    create_response = client.post(
        "/expenses/",
        json={
            "title": "Expense To Delete",
            "amount": 100,
            "category": "test"
        }
    )

    expense_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/expenses/{expense_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "expense deleted"

    get_response = client.get(
        f"/expenses/{expense_id}"
    )

    assert get_response.status_code == 404

def test_create_expense_invalid_amount():
    response = client.post(
        "/expenses/",
        json={
            "title": "Invalid expense",
            "amount": -100,
            "category": "food"
        }
    )
    assert response.status_code == 422

def test_create_expense_strips_whitespace():
    response = client.post(
        "/expenses/",
        json={
            "title": "   Lunch   ",
            "amount": 100,
            "category": "   food   "
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Lunch"
    assert data["category"] == "food"

def test_create_expense_rejects_blank_title():
    response = client.post(
        "/expenses/",
        json={
            "title": "     ",
            "amount": 100,
            "category": "food"
        }
    )

    assert response.status_code == 422

def test_update_expense_not_found():
    response = client.put(
        "/expenses/999999",
        json={
            "title": "Updated",
            "amount": 500,
            "category": "food"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_delete_expense_not_found():
    response = client.delete("/expenses/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"

def test_filter_expenses_by_category():
    client.post(
        "/expenses/",
        json={
            "title": "Lunch",
            "amount": 100,
            "category": "food"
        }
    )

    client.post(
        "/expenses/",
        json={
            "title": "Taxi",
            "amount": 200,
            "category": "transport"
        }
    )

    response = client.get("/expenses/?category=food")

    assert response.status_code == 200

    data = response.json()

    assert all(expense["category"] == "food" for expense in data)

def test_expense_pagination():
    for i in range(5):
        client.post(
            "/expenses/",
            json={
                "title": f"Expense {i}",
                "amount": 100,
                "category": "test"
            }
        )

    response = client.get("/expenses/?skip=0&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
def test_pagination_limit_validation():
    response = client.get("/expenses/?limit=101")

    assert response.status_code == 422
def test_pagination_negative_skip():
    response = client.get("/expenses/?skip=-1")

    assert response.status_code == 422