from flask import Flask
from routes.backup_upload import backup_upload_bp
from routes.backup_list import backup_list_bp
from routes.auth import auth_bp
from services.database import PostgresDB
from dotenv import load_dotenv
import os

URL_PREFIX = "/api"
load_dotenv()
app = Flask(__name__)

# Initialize the database
db = PostgresDB(
    dbname="media_backup", user="postgres", password="", host="localhost", port=5432
)
db.connect()

# Attach the the apps config
app.config["db"] = db
app.config["JWT_AUTH_TOKEN"] = os.getenv("JWT_AUTH_TOKEN")

# Register Blueprints
app.register_blueprint(backup_upload_bp, url_prefix=URL_PREFIX)
app.register_blueprint(backup_list_bp, url_prefix=URL_PREFIX)
app.register_blueprint(auth_bp, url_prefix=URL_PREFIX)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
