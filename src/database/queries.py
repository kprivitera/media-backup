INSERT_MEDIA_FILE = """
INSERT INTO media (filename, filepath, media_type, metadata_date, file_hash, user_id)
VALUES (%s, %s, %s, %s, %s, %s)
"""