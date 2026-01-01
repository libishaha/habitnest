from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import get_db_connection, create_user, get_user_by_email
from werkzeug.security import check_password_hash


main_routes = Blueprint("main_routes", __name__)

@main_routes.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "success", "message": "Database connected!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@main_routes.route("/signup", methods = ["POST"])
def signup():
    data = request.get_json()
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not username or not email or not password:
        return {"status" : "error", "message" : "All fields required"}, 400
    
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"status" : "error", "message" : "Email already registered"}), 400
    
    try:
        create_user(username, email, password)
        return jsonify({"status" : "success", "message" : "User created successfully"})
    except Exception as e:
        return jsonify({"status" : "error", "message" : str(e)}, 500)


@main_routes.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"status" : "error", "message" : "All fields required"}, 400)
    
    user = get_user_by_email(email)
    if not user:
        return jsonify({"status" : "error", "message" : "Invalid email or password"})
    
    if check_password_hash((user["password_hash"]), password):
        access_token = create_access_token(identity=str(user['id']))
        return jsonify({"status" : "success", 
                        "message" : "User logged in successfully",
                        "access_token" : access_token,
                        "user" : {
                            "id" : user['id'],
                            "username" : user['username'],
                            "email" : user['email']
                        }
                    })
    else:
        return jsonify({"status" : "error", "message" : "Invalid Email or Password"}), 401

@main_routes.route("/profile", methods = ["GET"])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    return jsonify({
        "status" : "success",
        "user-id" : current_user_id,
        "message" : "This is a protected route"
    }), 200

        
        
        