import jwt
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"


def generate_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data
        except Exception:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return wrapper

def generate_refresh_token(user):
    payload = {
        "user_id": user.id,
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")

            if not token:
                return jsonify({"message": "Token missing"}), 401

            try:
                token = token.split(" ")[1]
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_role = data.get("role")

                if user_role != required_role:
                    return jsonify({"message": "Forbidden"}), 403

            except Exception:
                return jsonify({"message": "Invalid token"}), 401

            return f(*args, **kwargs)

        return wrapper

    return decorator