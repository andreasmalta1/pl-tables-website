# import os
from flask import request, Blueprint, jsonify, session
from werkzeug.security import check_password_hash

from ...models import User

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"msg": "Invalid credentials"}), 401

        session["user_id"] = user.id
        return jsonify({"id": user.id, "email": user.email})


@auth_blueprint.route("/current-user", methods=["GET"])
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"msg": "Invalid credentials"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({"id": user.id, "email": user.email})
