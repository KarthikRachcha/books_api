import os
import mysql.connector
import json
from app.models.books_models import Book
from app.redis_client import redis_client

db_config = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME")
}

CACHE_EXPIRY = 300  # 5 minutes

class BooksService:

    @staticmethod
    def get_all_books():
        cached = redis_client.get("all_books")
        if cached:
            return [Book(**b) for b in json.loads(cached)]

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        redis_client.set("all_books", json.dumps(rows), ex=CACHE_EXPIRY)
        return [Book(**row) for row in rows]

    @staticmethod
    def get_book_by_id(book_id: int):
        cached = redis_client.get(f"book_{book_id}")
        if cached:
            return Book(**json.loads(cached))

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            redis_client.set(f"book_{book_id}", json.dumps(row), ex=CACHE_EXPIRY)
            return Book(**row)
        return None

    @staticmethod
    def add_book(book: Book):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)",
            (book.title, book.author, book.year)
        )
        conn.commit()
        book.id = cursor.lastrowid
        cursor.close()
        conn.close()

        # Invalidate cache
        redis_client.delete("all_books")
        return book

    @staticmethod
    def update_book(book_id: int, book: Book):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET title=%s, author=%s, year=%s WHERE id=%s",
            (book.title, book.author, book.year, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        # Invalidate cache
        redis_client.delete("all_books")
        redis_client.delete(f"book_{book_id}")
        book.id = book_id
        return book

    @staticmethod
    def delete_book(book_id: int):
        book = BooksService.get_book_by_id(book_id)
        if not book:
            return None

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
        conn.commit()
        cursor.close()
        conn.close()

        # Invalidate cache
        redis_client.delete("all_books")
        redis_client.delete(f"book_{book_id}")
        return book
