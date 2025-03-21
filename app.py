from datetime import datetime
from flask import Flask,jsonify,request
from models import Book,APIResponse,Author,User
from database import init_db,db
from services.book_service import BookService
from services.author_service import AuthorService
from services.user_service import UserService
from flask_swagger_ui import get_swaggerui_blueprint
import re
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
init_db(app)
with app.app_context():
    db.create_all()

SWAGGER_URL = "/swagger" 
API_URL = "/static/swagger.json"  

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL,config={
        "app_name": "Book API",
        "validatorUrl": None,
        "swaggerHeaders": [{"name": "Authorization", "value": "Bearer YOUR_JWT_TOKEN"}]
})
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


app.config["JWT_SECRET_KEY"] = "THIS_IS_MY_BOOK_STORE_JWT_AUTHENTICATION_KEY"
jwt = JWTManager(app)


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if "email" not in data or not data['email']:
            response = APIResponse(None, f"Email is required.", 400, False)
            return jsonify(response.to_dict()), 400

        if "password" not in data or not data['password']:
            response = APIResponse(None, f"Password is required.", 400, False)
            return jsonify(response.to_dict()), 400
        
        EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(EMAIL_REGEX, data['email']):
            response = APIResponse(None, f"Email must be valid.", 400, False)
            return jsonify(response.to_dict()), 400
        
        PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not re.match(PASSWORD_REGEX, data['password']):
            response = APIResponse(None, f"Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, one digit, and one special character.", 400, False)
            return jsonify(response.to_dict()), 400
        
        user = User(email=data["email"])
        user.set_password(data["password"])
        if UserService.register(user):
            response = APIResponse(None,"User registration successfully.",201,True)
            return jsonify(response.to_dict()),201
        
        else :
            response = APIResponse(None,"Email already register.",201,True)
            return jsonify(response.to_dict()),201
    
    except:
        response = APIResponse(None,"Error while registering user.",500,False)
        return jsonify(response.to_dict()),500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json

        if "email" not in data or not data['email']:
            response = APIResponse(None, f"Email is required.", 400, False)
            return jsonify(response.to_dict()), 400

        if "password" not in data or not data['password']:
            response = APIResponse(None, f"Password is required.", 400, False)
            return jsonify(response.to_dict()), 400
        
        user = User(email=data["email"],password=data["password"])

        if UserService.login(user):
            access_token = create_access_token(identity=user.email)
            response = APIResponse({"token":access_token}, f"Login successful.", 200, True)
            return jsonify(response.to_dict()), 200 
        else:
            response = APIResponse(None, f"Invalid email & password.", 401, False)
            return jsonify(response.to_dict()), 401 
        
    except:
        response = APIResponse(None,"Error while loging user.",500,False)
        return jsonify(response.to_dict()),500
    

@app.route('/books', methods=["GET"])
@jwt_required()
def get_all_books():
    try:
        if not request.args.get("currentPage"):
            response = APIResponse(None, "CurrentPage is required.", 400, False)
            return jsonify(response.to_dict()), 400

        if not request.args.get("rowsPerPage"):
            response = APIResponse(None, "RowsPerPage is required.", 400, False)
            return jsonify(response.to_dict()), 400

        currentPage = int(request.args.get("currentPage"))
        rowsPerPage = int(request.args.get("rowsPerPage"))
        order_by = request.args.get("orderBy", "asc").lower() 
        order_attribute = request.args.get("orderAttribute", "id").lower() 

        start_date = request.args.get("startDate",None)
        end_date = request.args.get("endDate",None)

        if currentPage <= 0 or rowsPerPage <= 0:
            response = APIResponse(None, "Current page and rows per page must be greater than 0.", 400, False)
            return jsonify(response.to_dict()), 400

        if order_by not in ["asc", "desc"]:
            response = APIResponse(None, "Invalid orderBy value. Use 'asc' or 'desc'.", 400, False)
            return jsonify(response.to_dict()), 400
        
        if order_attribute not in ["id", "price"]:
            response = APIResponse(None, "Invalid orderAttribute value. Use 'id' or 'price'.", 400, False)
            return jsonify(response.to_dict()), 400
        
        if start_date:
            try:
                parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                start_date = parsed_start_date
            except Exception as e:
                print(e)
                response = APIResponse(None, "Invalid start date format. Use YYYY-MM-DD.", 400, False)
                return jsonify(response.to_dict()), 400           
        if end_date:
            try:
                parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                end_date = parsed_end_date
            except:
                response = APIResponse(None, "Invalid end date format. Use YYYY-MM-DD.", 400, False)
                return jsonify(response.to_dict()), 400

        data = BookService.get_all_books(currentPage, rowsPerPage,start_date,end_date, order_by,order_attribute)
        if data:
            response = APIResponse(data, "Books fetched successfully.", 200, True)
            return jsonify(response.to_dict()), 200
        else:
            response = APIResponse(None, "No books available or invalid page number.", 404, False)
            return jsonify(response.to_dict()), 404
    except Exception as e:
        print(e)
        response = APIResponse(None, "Error while fetching books.", 500, False)
        return jsonify(response.to_dict()), 500


@app.route('/books/author/<int:author_id>', methods=["GET"])
@jwt_required() 
def get_books_by_author(author_id):
    try:
        currentPage = int(request.args.get("currentPage")) 
        rowsPerPage = int(request.args.get("rowsPerPage"))
        if currentPage<=0 or rowsPerPage<=0:
            print(currentPage)
            response = APIResponse(None,"Current page and rows per page must greater than 0.",400,False)
            return jsonify(response.to_dict()),400
        
        data = BookService.get_books_by_author(author_id,currentPage,rowsPerPage)
        if len(data["books"]) > 0:
            response = APIResponse(data,"Books fetched successfully.",200,True)
            return jsonify(response.to_dict()),200
        else:
            response = APIResponse(None,"No books available for author or invalid page number.",404,False)
            return jsonify(response.to_dict()),404
    except:
        response = APIResponse(None,"Error while fetching books.",500,False)
        return jsonify(response.to_dict()),500


@app.route('/books/search',methods=["GET"])
@jwt_required()
def search_book():
    try:
        if not request.args.get("title"):
            response = APIResponse(None, "Book title is required.", 400, False)
            return jsonify(response.to_dict()), 400
        
        title = request.args.get("title")
        book = BookService.search_book(title.lower())
        if book:
            response = APIResponse(book,"Book fetched successfully.",200,True)
            return jsonify(response.to_dict()),200
        else:
            response = APIResponse(None,"Book not found.",404,False)
            return jsonify(response.to_dict()),404
    except:
        response = APIResponse(None,"Error while searching book.",500,False)
        return jsonify(response.to_dict()),500


@app.route('/books/<int:book_id>', methods=["GET"])
@jwt_required() 
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
@jwt_required() 
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
@jwt_required() 
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
@jwt_required() 
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
@jwt_required() 
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
@jwt_required() 
def add_author():
    try:
        data = request.get_json()

        if "name" not in data or not data["name"] :
            response = APIResponse(None, f"Author name is required.", 400, False)
            return jsonify(response.to_dict()), 400
        
        author = Author(name=data["name"])
        AuthorService.add_author(author)

        response = APIResponse(None,"Author added successfully",201,True)
        return jsonify(response.to_dict()),201
    
    except:
        response = APIResponse(None,"Error while adding author.",500,False)
        return jsonify(response.to_dict()),500

@app.route('/authors/<int:author_id>', methods=["DELETE"])
@jwt_required() 
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
