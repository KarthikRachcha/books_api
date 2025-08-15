from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routers import books_routers


app=FastAPI(title= "Books API")

app.include_router(books_routers.router)

# This file is the entry point for the FastAPI application.
# It initializes the FastAPI app and includes the books router.


@app.get("/")
def root():
    return {"message": "Books API is running"}
