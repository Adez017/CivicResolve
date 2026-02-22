from flask import Blueprint, request, jsonify
from backend.models import db, User
from backend.utils.auth import generate_token
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    # user = User.query.filter_by(username=username, password=password).first()
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # if not user:
    #     return jsonify({"message": "Invalid credentials"}), 401

    token = generate_token(user)

    return jsonify({"token": token})