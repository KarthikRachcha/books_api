from fastapi import APIRouter, HTTPException, status
from app.services.books_services import BooksService
from app.models.books_models import Book

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[Book], status_code=status.HTTP_200_OK)
def get_books():
    books = BooksService.get_all_books()
    if books is None:
        raise HTTPException(status_code=500, detail="Database error")
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
def get_book(book_id: int):
    book = BooksService.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def add_book(book: Book):
    new_book = BooksService.add_book(book)
    if new_book is None:
        raise HTTPException(status_code=500, detail="Database error")
    return new_book

@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
def update_book(book_id: int, book: Book):
    updated_book = BooksService.update_book(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    deleted_book = BooksService.delete_book(book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
