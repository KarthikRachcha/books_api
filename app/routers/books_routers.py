from fastapi import APIRouter
from app.services.books_services import BooksService
from app.models.books_models import Book

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[Book])
def get_books():
    return BooksService.get_all_books()

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    return BooksService.get_book_by_id(book_id)

@router.post("/", response_model=Book)
def add_book(book: Book):  # <-- changed from books:Book to book:Book
    return BooksService.add_book(book)

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: Book):
    return BooksService.update_book(book_id, book)

@router.delete("/{book_id}", response_model=Book)
def delete_book(book_id: int):
    return BooksService.delete_book(book_id)