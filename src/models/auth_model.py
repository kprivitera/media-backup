import os
from functools import wraps
import jwt
from flask import request, jsonify, g, current_app

SECRET_KEY = os.getenv("JWT_AUTH_TOKEN")

def jwt_required(f):
    """Decorator to protect routes with JWT validation."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validation_result = validate_jwt()
        if isinstance(validation_result, tuple):  # If validation failed, return the error response
            return validation_result
        return f(*args, **kwargs)  # Proceed to the route if validation passed
    return decorated_function

def validate_jwt():
    """Validate the JWT from the Authorization header."""
    jwt_secret_key = current_app.config["JWT_AUTH_TOKEN"]
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 401

    try:
        # Extract the token from the "Bearer <token>" format
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
        g.decoded_token = decoded_token  # Store the decoded token in Flask's `g` object
        return decoded_token
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401