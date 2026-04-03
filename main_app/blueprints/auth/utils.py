# blueprints/auth/utils.py
from functools import wraps
from flask import session, jsonify


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"msg": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated_function
