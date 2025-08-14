import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.books_models import Book

client = TestClient(app)

def test_get_all_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_book():
    book_data = {
        "id": 100,
        "title": "Test Book",
        "author": "Test Author",
        "year": 2025
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_get_book_by_id():
    response = client.get("/books/100")
    assert response.status_code == 200
    assert response.json()["id"] == 100

def test_update_book():
    updated_data = {
        "id": 100,
        "title": "Updated Book",
        "author": "Updated Author",
        "year": 2026
    }
    response = client.put("/books/100", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"

def test_delete_book():
    response = client.delete("/books/100")
    assert response.status_code == 200
    assert response.json()["id"] == 100

def test_book_not_found():
    response = client.get("/books/9999")
    assert response.status_code == 404
