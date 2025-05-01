import os
from flask import Blueprint, request, current_app
import jwt
from datetime import datetime, timedelta

# Create a Blueprint for the login route
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    jwt_secret_key = current_app.config["JWT_AUTH_TOKEN"]
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "password":  # Replace with real validation
        # Generate a JWT token
        token = jwt.encode(
            {
                "username": username,
                "id": 1,  # Example user ID
                "exp": datetime.utcnow()
                + timedelta(hours=1),  # Token expires in 1 hour
            },
            jwt_secret_key,
            algorithm="HS256",
        )
        return {"token": token}, 200
    else:
        return {"error": "Invalid credentials"}, 401
