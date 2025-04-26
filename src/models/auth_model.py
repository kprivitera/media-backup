from functools import wraps
import jwt
from flask import request, jsonify, g

SECRET_KEY = "your-very-secure-secret-key"

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
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Authorization header is missing"}), 401

    try:
        # Extract the token from the "Bearer <token>" format
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        g.decoded_token = decoded_token  # Store the decoded token in Flask's `g` object
        return decoded_token
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401