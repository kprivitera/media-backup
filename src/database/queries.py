INSERT_MEDIA_FILE = """
INSERT INTO media (filename, filepath, media_type, metadata_date, file_hash, user_id)
VALUES (%s, %s, %s, %s, %s, %s)
"""

RETRIEVE_MEDIA_BY_DATE = """
SELECT *
FROM media
WHERE EXTRACT(MONTH FROM upload_date) = %s
  AND EXTRACT(YEAR FROM upload_date) = %s
  AND user_id = %s
"""
