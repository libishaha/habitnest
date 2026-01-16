from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import get_db_connection, create_user, get_user_by_email, create_task, toggle_task_complete, delete_task, get_tasks_by_date
from werkzeug.security import check_password_hash
from datetime import date


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

@main_routes.route("/tasks", methods = ["POST"])
@jwt_required()
def add_task():
    current_user = get_jwt_identity()
    
    data = request.get_json()
    task_text = data.get("task_text")
    task_date = data.get("task_date")
    
    if not task_text:
        return jsonify({"status" : "error", "message" : "Task text is required"}),400
    
    if not task_date:
        task_date = str(date.today())
    
    try:
        task_id = create_task(int(current_user), task_text, task_date)
        return jsonify({"status" : "success", "message" : "Task created", "task_id" : task_id}), 201
    except Exception as e:
        return jsonify({"ststus" : "error", "message" : str(e)}), 500

@main_routes.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    
    task_date = request.args.get("date", str(date.today()))
    
    try:
        tasks = get_tasks_by_date(int(current_user_id), task_date)
        return jsonify({
            "status": "success",
            "tasks": tasks,
            "date": task_date
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@main_routes.route("/tasks/<int:task_id>/toggle", methods=["PUT"])
@jwt_required()
def toggle_task(task_id):
    current_user_id = get_jwt_identity()
    
    try:
        success = toggle_task_complete(task_id, int(current_user_id))
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Task updated"
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Task not found or unauthorized"
            }), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500