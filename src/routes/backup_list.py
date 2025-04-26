from flask import Blueprint, request, g, current_app

# Create a Blueprint for the upload route
backup_list_bp = Blueprint("backup_list", __name__)

@backup_list_bp.route('/backups', methods=['GET'])
def list_photos():
    """List all uploaded photos with basic metadata."""
    try:
        photos = []
        for filename in os.listdir(Config.UPLOAD_FOLDER):
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                stats = os.stat(file_path)
                photos.append({
                    'filename': filename,
                    'size': stats.st_size,  # Size in bytes
                    'uploaded_at': stats.st_mtime  # Modification time as upload time
                })
        return jsonify({'photos': photos}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to list photos: {str(e)}'}), 500