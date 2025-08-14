import os
import mysql.connector
from app.models.books_models import Book

# Database configuration using environment variables
db_config = {
    "host": os.environ.get("DB_HOST", "34.171.157.123"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", "YOUR_PASSWORD"),
    "database": os.environ.get("DB_NAME", "books_db")
}

class BooksService:

    @staticmethod
    def get_all_books():
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Book(**row) for row in rows]

    @staticmethod
    def get_book_by_id(book_id: int):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Book(**row)
        return None

    @staticmethod
    def add_book(book: Book):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, published_year, genre) VALUES (%s, %s, %s, %s)",
            (book.title, book.author, book.published_year, book.genre)
        )
        conn.commit()
        book.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return book

    @staticmethod
    def update_book(book_id: int, book: Book):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET title=%s, author=%s, published_year=%s, genre=%s WHERE id=%s",
            (book.title, book.author, book.published_year, book.genre, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
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
        return book
