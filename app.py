from flask import Flask,jsonify,request
from models import Book,APIResponse,Author
from database import init_db,db
from service import BookService,AuthorService
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
init_db(app)
with app.app_context():
    db.create_all()

SWAGGER_URL = "/swagger" 
API_URL = "/static/swagger.json"  

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/books', methods=["GET"])
def get_all_books():
    try:
        currentPage = int(request.args.get("currentPage")) 
        rowsPerPage = int(request.args.get("rowsPerPage"))
        if currentPage<=0 or rowsPerPage<=0:
            print(currentPage)
            response = APIResponse(None,"Current page and rows per page must greater than 0.",400,False)
            return jsonify(response.to_dict()),400
        
        data = BookService.get_all_books(currentPage,rowsPerPage)
        if data:
            response = APIResponse(data,"Books fetched successfully.",200,True)
            return jsonify(response.to_dict()),200
        else:
            response = APIResponse(None,"No books available or invalid page number.",404,False)
            return jsonify(response.to_dict()),404
    except:
        response = APIResponse(None,"Error while fetching books.",500,False)
        return jsonify(response.to_dict()),500
  
    
@app.route('/books/author/<int:author_id>', methods=["GET"])
def get_books_by_author(author_id):
    try:
        currentPage = int(request.args.get("currentPage")) 
        rowsPerPage = int(request.args.get("rowsPerPage"))
        if currentPage<=0 or rowsPerPage<=0:
            print(currentPage)
            response = APIResponse(None,"Current page and rows per page must greater than 0.",400,False)
            return jsonify(response.to_dict()),400
        
        data = BookService.get_books_by_author(author_id,currentPage,rowsPerPage)
        if data:
            response = APIResponse(data,"Books fetched successfully.",200,True)
            return jsonify(response.to_dict()),200
        else:
            response = APIResponse(None,"No books available or invalid page number.",404,False)
            return jsonify(response.to_dict()),404
    except:
        response = APIResponse(None,"Error while fetching books.",500,False)
        return jsonify(response.to_dict()),500


@app.route('/books/<int:book_id>', methods=["GET"])
def get_book(book_id):
    try:
        book = BookService.get_book(book_id)
        if book:
            response = APIResponse(book,"Book fetched successfully.",200,True)
            return jsonify(response.to_dict()),200
        else:
            response = APIResponse(None,"Book not found.",404,False)
            return jsonify(response.to_dict()),404
    except:
        response = APIResponse(None,"Error while fetching book.",500,False)
        return jsonify(response.to_dict()),500


@app.route('/books', methods=["POST"])
def add_book():
    try:
        data = request.get_json()

        required_fields = ["title", "isbn", "price", "author_id"]
        for field in required_fields:
            if field not in data or not data[field]:
                response = APIResponse(None, f"Book {field} is required.", 400, False)
                return jsonify(response.to_dict()), 400
            
        if data["price"] < 0:
            response = APIResponse(None, "Book price must be greater than zero.", 400, False)
            return jsonify(response.to_dict()), 400
        
        if not data["isbn"].isdigit():
            response = APIResponse(None, "Book ISBN must be a number.", 400, False)
            return jsonify(response.to_dict()), 400
        
        if len(data["isbn"]) not in [10, 13]:
            response = APIResponse(None, "Book ISBN must have 10 or 13 digits.", 400, False)
            return jsonify(response.to_dict()), 400
        
        book = Book(title=data["title"], isbn=data["isbn"], price=data["price"],author_id=data["author_id"])
        temp = BookService.add_book(book)
        
        if temp == "added":
            response = APIResponse(None,"Book added successfully",201,True)
            return jsonify(response.to_dict()),201
        elif temp == "isbn_exists":
            response = APIResponse(None,"Book ISBN must be unique.",400,False)
            return jsonify(response.to_dict()),400
        else:
            response = APIResponse(None,"Invalid author_id",400,False)
            return jsonify(response.to_dict()),400

    except:
        response = APIResponse(None,"Error while adding book.",500,False)
        return jsonify(response.to_dict()),500


@app.route('/books/<int:book_id>', methods=["PUT"])
def update_book(book_id):
    try:
        data = request.get_json()

        required_fields = ["title", "isbn", "price", "author_id"]
        for field in required_fields:
            if field in data and not data[field]:
                response = APIResponse(None, f"Book {field} is required.", 400, False)
                return jsonify(response.to_dict()), 400
            
        if "price" in data and data["price"] < 0:
            response = APIResponse(None, "Book price must be greater than zero.", 400, False)
            return jsonify(response.to_dict()), 400

        if "isbn" in data:
            if not data["isbn"].isdigit():
                response = APIResponse(None, "Book ISBN must be a number.", 400, False)
                return jsonify(response.to_dict()), 400
            if len(data["isbn"]) not in [10, 13]:
                response = APIResponse(None, "Book ISBN must have 10 or 13 digits.", 400, False)
                return jsonify(response.to_dict()), 400
            
        
        status, book = BookService.update_book(book_id, data)

        if status == "update":
            response = APIResponse(book, "Book updated successfully.", 200, True)
            return jsonify(response.to_dict()), 200
        elif status == "isbn_exists":
            response = APIResponse(None, "Book ISBN must be unique.", 400, False)
            return jsonify(response.to_dict()), 400
        else:
            response = APIResponse(None, "Book not found.", 404, False)
            return jsonify(response.to_dict()), 404
        
    except:
        response = APIResponse(None,"Error while updating book.",500,False)
        return jsonify(response.to_dict()),500
    
    
@app.route('/books/<int:book_id>', methods=["DELETE"])
def delete_book(book_id):
    try:
        deleted = BookService.delete_book(book_id)
        if deleted:
            response = APIResponse(None, "Book deleted successfully.", 200, True)
            return jsonify(response.to_dict()), 200
        else:
            response = APIResponse(None, "Book not found.", 404, False)
            return jsonify(response.to_dict()), 404
    except:
        response = APIResponse(None,"Error while deleting book.",500,False)
        return jsonify(response.to_dict()),500


@app.route('/authors', methods=["GET"])
def get_all_authors():
    try:
        authors = AuthorService.get_all_authors()
        if authors:
            response = APIResponse(authors,"Authors fetched successfully.",200,True)
            return jsonify(response.to_dict()),200
        else:
            response = APIResponse(None,"No Authors available.",404,False)
            return jsonify(response.to_dict()),404
    except:
        response = APIResponse(None,"Error while fetching books.",500,False)
        return jsonify(response.to_dict()),500


@app.route('/authors', methods=["POST"])
def add_author():
    data = request.get_json()

    if "name" not in data or not data["name"] :
        response = APIResponse(None, f"Author name is required.", 400, False)
        return jsonify(response.to_dict()), 400
    
    author = Author(name=data["name"])
    AuthorService.add_author(author)

    response = APIResponse(None,"Author added successfully",201,True)
    return jsonify(response.to_dict()),201

@app.route('/authors/<int:author_id>', methods=["DELETE"])
def delete_author(author_id):
    try:
        deleted = AuthorService.delete_author(author_id)
        if deleted:
            response = APIResponse(None, "Author deleted successfully.", 200, True)
            return jsonify(response.to_dict()), 200
        else:
            response = APIResponse(None, "Author not found.", 404, False)
            return jsonify(response.to_dict()), 404
    except:
        response = APIResponse(None,"Error while deleting author.",500,False)
        return jsonify(response.to_dict()),500

if __name__ == "__main__":
    app.run(debug=True)
