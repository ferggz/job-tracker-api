from functools import wraps
from flask import jsonify, session


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "You must be logged in"}), 401

        return func(*args, **kwargs)

    return wrapper