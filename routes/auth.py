from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from database import get_db_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    password_hash = generate_password_hash(password)

    conn = get_db_connection()

    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
    except Exception:
        conn.close()
        return jsonify({"error": "Username already exists"}), 409

    conn.close()

    return jsonify({"message": "User registered successfully"}), 201


from werkzeug.security import check_password_hash

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful"}), 200