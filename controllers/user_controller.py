from flask import Blueprint, jsonify, request
from models.api_response import APIResponse
from models.user import User
from services.user_service import UserService
from flask_jwt_extended import create_access_token
import re

user_bp = Blueprint("user_bp", __name__)

@user_bp.route('/register', methods=['POST'])
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


@user_bp.route("/login", methods=["POST"])
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
    