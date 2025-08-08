from flask import Blueprint, request, jsonify

login_bp = Blueprint('login_bp', __name__)

USERNAME = "admin"
PASSWORD = "password123"

@login_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    if data.get("username") == USERNAME and data.get("password") == PASSWORD:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401
