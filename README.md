Follow the steps below to set up and run the Book Store API locally.

1. Prerequisites :
    * Python 3.10
    * PostgreSQL
    * Docker

2. Clone the Repository :
    * git clone https://github.com/mj986903/Book-Store-Python.git
    * cd Book-Store-Python

3. Create docker image :
    * docker build -t <image-name> .

4. Run app :
    * docker run -p 5000:5000 <image-name>

5. Access the API :
    * Swagger Documentation: http://localhost:5000/swagger
    * API Base URL: http://localhost:5000/

6. API Endpoints :

    * POST   /register                  -> Register a new user
    * POST   /login                     -> Login user

    * GET    /books                     -> List all books with filters
    * POST   /books                     -> Add a new book
    * GET    /books/search              -> Search books
    * GET    /books/author/{author_id}  -> List books by author ID
    * GET    /books/{book_id}           -> Get book by ID
    * PUT    /books/{book_id}           -> Update book by ID
    * DELETE /books/{book_id}           -> Delete book by ID

    * GET    /authors                   -> List all authors
    * POST   /authors                   -> Add a new author
    * DELETE /authors/{author_id}       -> Delete author by ID
