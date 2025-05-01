from flask import Blueprint, request, g, current_app
from utils.metadata_utils import get_date_by_file_type
from models.backup_upload_model import (
    save_file,
    generate_unique_filename,
    compute_file_hash,
    insert_file_metadata,
    check_file_hash_exists
)
from models.auth_model import jwt_required
import os
from datetime import datetime

UPLOAD_FOLDER = "backups"
UPLOAD_KEY = "file"

# Create a Blueprint for the upload route
backup_upload_bp = Blueprint("backup_upload", __name__)


@backup_upload_bp.route("/backups", methods=["POST"])
@jwt_required
def upload_file():
    # Access the decoded token
    decoded_token = g.decoded_token
    user_id = decoded_token.get("id")

    # Create a directory for the authenticated user
    user_directory = os.path.join(UPLOAD_FOLDER, str(user_id))
    os.makedirs(user_directory, exist_ok=True)

    # Validate image is in the request
    if UPLOAD_KEY not in request.files:
        return "No file uploaded", 400

    file = request.files[UPLOAD_KEY]
    media_type = (
        "image"
        if file.mimetype.startswith("image/")
        else "video" if file.mimetype.startswith("video/") else None
    )

    # Validate filename exists
    if file.filename == "":
        return "No filename set", 400

    # Validate file type
    if not (file.mimetype.startswith("image/") or file.mimetype.startswith("video/")):
        return "Unsupported file type", 415

    # Process metadata
    date = get_date_by_file_type(file)
    print(f"Extracted date: {date}")
    if date is None:
        return "Invalid or unsupported metadata", 415

    # Convert date to ISO 8601 format
    try:
        metadata_date = datetime.strptime(date, "%Y:%m:%d").date().isoformat()
    except ValueError:
        return "Invalid date format in metadata", 415

    # Save the file
    generated_filename = generate_unique_filename(file)
    file_path = save_file(file, user_directory, generated_filename)

    # Generate file hash
    file_hash = compute_file_hash(file)
    print(f"File hash: {file_hash}")

    # Check if the file hash already exists in the database
    db = current_app.config["db"]
    try:
        if check_file_hash_exists(db, file_hash):
            return "File already exists", 409
    except Exception as e:
        return f"Error checking file hash: {e}", 500

    print(f"File hash: {file_hash}")

    # Insert metadata into the database
    try:
        insert_file_metadata(
            db, file.filename, file_path, media_type, metadata_date, file_hash, user_id
        )
    except Exception as e:
        return f"Error saving to database: {e}", 500

    return f"Saved to {file_path}", 200
