from flask import Blueprint, jsonify, request
from models.api_response import APIResponse
from models.author import Author
from services.author_service import AuthorService
from flask_jwt_extended import jwt_required

author_bp = Blueprint("author_bp", __name__)

@author_bp.route('/authors', methods=["GET"])
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


@author_bp.route('/authors', methods=["POST"])
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

@author_bp.route('/authors/<int:author_id>', methods=["DELETE"])
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
