from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
import sqlite3
import asyncio
import random 
import requests



# Initialize FastAPI application
app = FastAPI()

# Function to establish a connection to the SQLite database
def elaunch_new_database_connection():
    return sqlite3.connect("book_review_database.db")

# Function to create necessary tables if they don't already exist
def set_database():
    with elaunch_new_database_connection() as connection:
        cursor = connection.cursor()
        # Create books table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                        (book_id INTEGER PRIMARY KEY, book_title TEXT, book_author TEXT, publication_year INTEGER)''')
        # Create reviews table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS reviews 
                        (review_id INTEGER PRIMARY KEY, book_id INTEGER, review_text TEXT, review_rating INTEGER)''')
        connection.commit()

# Define Pydantic models for data validation
class NewBookModel(BaseModel):
    title_of_book: str
    author_of_book: str
    year_of_publication: int

class NewReviewModel(BaseModel):
    review_text: str
    review_rating: int

# Create necessary tables if they don't already exist
set_database()

# Part 1: API Endpoints with Data Validation and Error Handling

@app.post("/add-new-book/", status_code=201)
def add_original_book(original_book_details: NewBookModel):
    with elaunch_new_database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO books (book_title, book_author, publication_year) VALUES (?, ?, ?)",
                    (original_book_details.title_of_book, original_book_details.author_of_book, original_book_details.year_of_publication))
        connection.commit()
        book_id = cursor.lastrowid 
    return {"message": "The book has been successfully added to the database", "book_id": book_id}

@app.post("/add-new-book/", status_code=201)
def add_original_book(original_book_details: NewBookModel):
    with elaunch_new_database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO books (book_title, book_author, publication_year) VALUES (?, ?, ?)",
                    (original_book_details.title_of_book, original_book_details.author_of_book, original_book_details.year_of_publication))
        connection.commit()
    return {"message": "The book has been successfully added to the database"}

@app.post("/add-new-review/{book_id}/", status_code=201)
def add_authentic_review_for_book(book_id: int, authentic_review_details: NewReviewModel, background_tasks: BackgroundTasks):
    with elaunch_new_database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="The specified book does not exist in the database")
        
        cursor.execute("INSERT INTO reviews (book_id, review_text, review_rating) VALUES (?, ?, ?)",
                       (book_id, authentic_review_details.review_text, authentic_review_details.review_rating))
        connection.commit()

        # Schedule background task to send confirmation email
        background_tasks.add_task(send_confirmation_email, book_id)
        
        return {"message": "The review has been successfully added for the specified book"}

# Background task to simulate sending confirmation email
async def send_confirmation_email(book_id: int):
    await asyncio.sleep(random.randint(3, 7))  # Simulate email sending with random delay
    print(f"Confirmation email has been sent for book ID {book_id}")

# Endpoint to list books
@app.get("/list-books/", response_model=list[NewBookModel])
def list_books(author: str = None, publication_year: int = None):
    with elaunch_new_database_connection() as connection:
        cursor = connection.cursor()
        query = "SELECT * FROM books"
        if author and publication_year:
            query += f" WHERE book_author='{author}' AND publication_year={publication_year}"
        elif author:
            query += f" WHERE book_author='{author}'"
        elif publication_year:
            query += f" WHERE publication_year={publication_year}"
        
        cursor.execute(query)
        books = cursor.fetchall()
        
        # Convert the fetched data into dictionaries
        book_dicts = []
        for book in books:
            book_dict = {
                "title_of_book": book[1],
                "author_of_book": book[2],
                "year_of_publication": book[3]
            }
            book_dicts.append(book_dict)
        
        return book_dicts

# Endpoint to list reviews for a specific book
@app.get("/check_of_all_list_reviews/{book_id}/", response_model=list[NewReviewModel])
def list_reviews(book_id: int):
    with elaunch_new_database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM reviews WHERE book_id=?", (book_id,))
        reviews = cursor.fetchall()
        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found for this book")
        
        # Convert the fetched data into dictionaries
        review_dicts = []
        for review in reviews:
            review_dict = {
                "review_text": review[2],
                "review_rating": review[3]
            }
            review_dicts.append(review_dict)
        
        return review_dicts

# Part 2: CRUD Operations

@app.put("/update-book/{book_id}/", status_code=200)
def update_book_details(book_id: int, updated_book_details: NewBookModel):
    with elaunch_new_database_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE books SET book_title=?, book_author=?, publication_year=? WHERE book_id=?",
                       (updated_book_details.title_of_book, updated_book_details.author_of_book, updated_book_details.year_of_publication, book_id))
        connection.commit()
    return {"message": "The details of the specified book have been successfully updated"}

@app.delete("/delete-entry/{entry_id}/", status_code=200)
def remove_entry_list(entry_id: int):
    with elaunch_new_database_connection() as db_conn:
        cursor = db_conn.cursor()
        cursor.execute("DELETE FROM records WHERE entry_id=?", (entry_id,))
        db_conn.commit()
    return {"message": "Entry successfully deleted from the database"}





# Testing endpoint
# @app.get("/automate-test-endpoint-book/")
# def test_endpoint():
#     return {"message": "The test endpoint is functioning properly"}





@app.get("/automate-test-endpoint-book/")
def automate_test_endpoint_book():
    # Test adding a new book
    original_book = NewBookModel(title_of_book="Test Book", author_of_book="Test Author", year_of_publication=2022)
    response_add_book = requests.post("http://127.0.0.1:8000/add-new-book/", json=original_book.dict())
    if response_add_book.status_code != 201:
        return {"error": "Failed to add new book", "details": response_add_book.json()}
    
    # Test listing books
    response_alllist_books = requests.get("http://127.0.0.1:8000/list-books/")
    if response_alllist_books.status_code != 200:
        return {"error": "Failed to list books", "details": response_alllist_books.json()}
    
    # Test adding a new review for the added book
    book_id = response_add_book.json()["book_id"]
    authentic_review = NewReviewModel(review_text="Test Review", review_rating=5)
    response_add_review = requests.post(f"http://127.0.0.1:8000/add-new-review/{book_id}/", json=authentic_review.dict())
    if response_add_review.status_code != 201:
        return {"error": "Failed to add new review", "details": response_add_review.json()}
    
    # Test listing reviews for the added book
    response_list_reviews = requests.get(f"http://127.0.0.1:8000/check_of_all_list_reviews/{book_id}/")
    if response_list_reviews.status_code != 200:
        return {"error": "Failed to list reviews", "details": response_list_reviews.json()}
    
    # All tests passed
    return {"message": "All book-related tests passed successfully"}


# Testing background task
@app.post("/dynamic-test-email/{book_id}/", status_code=201)
def test_email_confirmation(book_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_confirmation_email, book_id)
    return {"message": f"A test email task for book {book_id} has been successfully scheduled"}

