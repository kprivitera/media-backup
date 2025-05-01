import os
import uuid
import hashlib
from database.queries import INSERT_MEDIA_FILE


def generate_unique_filename(file):
    file_extension = os.path.splitext(file.filename)[1]
    return f"{uuid.uuid4()}{file_extension}"


def compute_file_hash(file):
    """
    Compute the SHA-256 hash of a file.

    Args:
        file: A file-like object.

    Returns:
        str: The hexadecimal representation of the file's hash.
    """
    hasher = hashlib.sha256()
    file.seek(0)  # Ensure the file pointer is at the beginning
    while chunk := file.read(8192):  # Read the file in chunks
        if isinstance(chunk, str):  # Handle text mode files
            chunk = chunk.encode('utf-8')
        hasher.update(chunk)
    file.seek(0)  # Reset file pointer after reading
    return hasher.hexdigest()

def check_file_hash_exists(db, file_hash):
    query = "SELECT 1 FROM media WHERE file_hash = %s LIMIT 1"
    result = db.execute_query(query, (file_hash,))
    return bool(result)


def save_file(file, upload_folder, filename):
    print(f"save_file: {upload_folder} {filename}")
    filepath = os.path.join(upload_folder, filename)
    os.makedirs(upload_folder, exist_ok=True)
    file.save(filepath)
    return filepath


def insert_file_metadata(
    db, filename, file_path, media_type, metadata_date, file_hash, user_id
):
    query = INSERT_MEDIA_FILE
    params = (filename, file_path, media_type, metadata_date, file_hash, user_id)
    db.execute_query(query, params)
