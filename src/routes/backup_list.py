from flask import Blueprint, request, g, current_app
from models.auth_model import jwt_required
import os

# Create a Blueprint for the upload route
backup_list_bp = Blueprint("backup_list", __name__)


@backup_list_bp.route('/backups', methods=['GET'])
@jwt_required
def list_photos():
    """List all uploaded photos with basic metadata."""
    # Access the decoded token
    decoded_token = g.decoded_token
    user_id = decoded_token.get("id")
    print(user_id)

    # Get the list of files for the authenticated user
    user_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    if not os.path.exists(user_directory):
        return {"error": "No backups found"}, 404
