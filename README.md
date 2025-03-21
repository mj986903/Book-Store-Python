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

    * Register a new user  
        * Method: POST  
        * URL: /register  

    * Login user  
        * Method: POST  
        * URL: /login  

    * List books by author with pagination 
        * Method: GET  
        * URL: /books/author/{author_id}?currentPage={page}&rowsPerPage={rows} 

    * List books with pagination and filtering 
        * Method: GET  
        * URL: /books?currentPage={page}&rowsPerPage={rows}&orderBy={asc/desc}&orderAttribute={id/price}&startDate={YYYY-MM-DD}&endDate={YYYY-MM-DD}  

    * Add a new book  
        * Method: POST  
        * URL: /books  

    * Search book by title
        * Method: GET  
        * URL: /books/search?title={title}  

    * Get book by ID  
        * Method: GET  
        * URL: /books/{book_id}  

    * Update book by ID  
        * Method: PUT  
        * URL: /books/{book_id}  

    * Delete book by ID 
        * Method: DELETE  
        * URL: /books/{book_id}  

    * List all authors 
        * Method: GET  
        * URL: /authors  

    * Add a new author  
        * Method: POST  
        * URL: /authors  

    * Delete author by ID  
        * Method: DELETE  
        * URL: /authors/{author_id}  

