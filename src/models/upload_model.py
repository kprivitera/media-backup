import os
import uuid
import hashlib
from database.queries import INSERT_MEDIA_FILE


def generate_unique_filename(file):
    file_extension = os.path.splitext(file.filename)[1]
    return f"{uuid.uuid4()}{file_extension}"


def compute_file_hash(file):
    hasher = hashlib.sha256()
    while chunk := file.read(8192):  # Read the file in chunks
        hasher.update(chunk)
    file.seek(0)  # Reset file pointer after reading
    return hasher.hexdigest()


def save_file(file, upload_folder, filename):
    print(f"save_file: {upload_folder} {filename}")
    filepath = os.path.join(upload_folder, filename)
    os.makedirs(upload_folder, exist_ok=True)
    file.save(filepath)
    return filepath

def insert_file_metadata(db, filename, file_path, media_type, metadata_date, file_hash, user_id):
    """Inserts file metadata into the database."""
    query = INSERT_MEDIA_FILE
    params = (filename, file_path, media_type, metadata_date, file_hash, user_id)
    db.execute_query(query, params)