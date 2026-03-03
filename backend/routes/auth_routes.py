from flask import Blueprint, request, jsonify
from backend.models import db, User
from backend.utils.auth import generate_token, generate_refresh_token
import jwt
from backend.utils.auth import SECRET_KEY

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username, password=password).first()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = generate_token(user)
    refresh_token = generate_refresh_token(user)

    user.refresh_token = refresh_token
    db.session.commit()

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.json
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"message": "Refresh token missing"}), 400

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])

        user = User.query.get(payload["user_id"])

        if not user or user.refresh_token != refresh_token:
            return jsonify({"message": "Invalid refresh token"}), 401

        new_access_token = generate_token(user)

        return jsonify({
            "access_token": new_access_token
        })

    except Exception:
        return jsonify({"message": "Invalid or expired refresh token"}), 401