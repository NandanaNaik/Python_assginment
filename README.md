# Python_assginment

The Book Review API provides endpoints to manage books and reviews. It allows users to add new books, add reviews for existing books, list all books, and list reviews for specific books.

## Features

- **Add New Book:** Users can add a new book to the database by providing details such as the title, author, and publication year.
- **Add New Review:** Users can add a new review for a specific book, including the review text and rating.
- **List Books:** Retrieve a list of all books stored in the database.
- **List Reviews:** View all reviews for a particular book.
- **Background Task:** Simulates sending a confirmation email after a review is posted.

## Setup

Follow these steps to set up and run the Book Review API:

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Ensure you have SQLite installed on your machine or update the database connection function to use a different database.
4. Run the FastAPI application using the command `uvicorn main:app --reload`.

## API Endpoints

### Add New Book
- **URL:** `/add-new-book/`
- **Method:** POST
- **Description:** Adds a new book to the database.
- **Request Body:** JSON object with the following fields:
  - `title_of_book`: Title of the book (string).
  - `author_of_book`: Author of the book (string).
  - `year_of_publication`: Year of publication (integer).
- **Response:** JSON object with a success message and the `book_id`.

### Add New Review
- **URL:** `/add-new-review/{book_id}/`
- **Method:** POST
- **Description:** Adds a new review for a specific book.
- **Request Body:** JSON object with the following fields:
  - `review_text`: Text of the review (string).
  - `review_rating`: Rating of the review (integer).
- **Response:** JSON object with a success message.

### List Books
- **URL:** `/list-books/`
- **Method:** GET
- **Description:** Retrieves a list of all books in the database.
- **Response:** JSON array containing details of all books.

### List Reviews
- **URL:** `/check_of_all_list_reviews/{book_id}/`
- **Method:** GET
- **Description:** Retrieves all reviews for a specific book.
- **Response:** JSON array containing details of all reviews for the specified book.

## Testing

To test the API endpoints, use the provided test endpoint `/automate-test-endpoint-book/`. This endpoint performs automated tests for adding a new book, listing books, adding a review, and listing reviews.

## Background Task

The API includes a background task to simulate sending a confirmation email after a review is posted. The task is scheduled asynchronously using `BackgroundTasks`.

## Dependencies

- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- Pydantic: Data validation and settings management using Python type annotations.
- SQLite: A lightweight, serverless, relational database management system.
- Requests: An elegant and simple HTTP library for Python, used for making HTTP requests.
- Uvicorn: A lightning-fast ASGI server implementation, used to run the FastAPI application.

**Happy coding!**

