import requests
import time

BASE_URL = "http://127.0.0.1:8000/books/"

def fetch_books():
    start = time.time()
    response = requests.get(BASE_URL)
    elapsed = time.time() - start
    source = response.headers.get("X-Cache-Status", "MISS")  # Optional header
    return response, elapsed, source

# First GET (should hit MySQL)
print("=== First GET request (expect MISS / MySQL) ===")
response, elapsed, source = fetch_books()
print("Status:", response.status_code)
print("Number of books:", len(response.json()))
print("Time taken:", round(elapsed, 4), "seconds")
print("Cache status:", source, "\n")

# Second GET (should hit Redis)
print("=== Second GET request (expect HIT / Redis) ===")
response, elapsed, source = fetch_books()
print("Status:", response.status_code)
print("Number of books:", len(response.json()))
print("Time taken:", round(elapsed, 4), "seconds")
print("Cache status:", source, "\n")

# Add new book (invalidates cache)
print("=== Adding a new book (invalidate cache) ===")
new_book = {
    "title": "Redis Test Book",
    "author": "Test Author",
    "year": 2025
}
response = requests.post(BASE_URL, json=new_book)
print("POST status:", response.status_code)
book_id = response.json()["id"]
print("New book ID:", book_id, "\n")

# GET after POST (should hit MySQL again)
print("=== GET after POST (expect MISS / MySQL) ===")
response, elapsed, source = fetch_books()
print("Status:", response.status_code)
print("Number of books:", len(response.json()))
print("Time taken:", round(elapsed, 4), "seconds")
print("Cache status:", source, "\n")

# Clean up: delete test book
print("=== Cleaning up (delete test book) ===")
delete_url = f"{BASE_URL}{book_id}"
response = requests.delete(delete_url)
print("DELETE status:", response.status_code)
