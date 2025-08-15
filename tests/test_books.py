import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.books_models import Book

client = TestClient(app)

def test_get_all_books():
    response = client.get("/books/")
    # 200 OK if books exist, 404 if empty
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert isinstance(response.json(), list)

def test_add_book():
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "year": 2025
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201  # POST now returns 201
    assert response.json()["title"] == "Test Book"

def test_get_book_by_id():
    # First add a book to ensure it exists
    book_data = {
        "title": "Get Test Book",
        "author": "Get Author",
        "year": 2025
    }
    post_resp = client.post("/books/", json=book_data)
    book_id = post_resp.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id

def test_update_book():
    # First add a book
    book_data = {
        "title": "Update Test Book",
        "author": "Update Author",
        "year": 2025
    }
    post_resp = client.post("/books/", json=book_data)
    book_id = post_resp.json()["id"]

    updated_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "year": 2026
    }
    response = client.put(f"/books/{book_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"

def test_delete_book():
    # First add a book
    book_data = {
        "title": "Delete Test Book",
        "author": "Delete Author",
        "year": 2025
    }
    post_resp = client.post("/books/", json=book_data)
    book_id = post_resp.json()["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204  # DELETE returns 204 No Content

def test_book_not_found():
    response = client.get("/books/999999")
    assert response.status_code == 404
