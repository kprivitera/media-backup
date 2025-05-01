from flask import Flask
from config import DevelopmentConfig
from routes.backup_upload import backup_upload_bp
from routes.backup_list import backup_list_bp
from routes.auth import auth_bp
from services.database import PostgresDB

URL_PREFIX = "/api"
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize the database
db_config = app.config["DATABASE"]
db = PostgresDB(
    dbname=db_config["dbname"],
    user=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    port=db_config["port"],
)
db.connect()

# Attach the the apps config
app.config["db"] = db

# Register Blueprints
app.register_blueprint(backup_upload_bp, url_prefix=URL_PREFIX)
app.register_blueprint(backup_list_bp, url_prefix=URL_PREFIX)
app.register_blueprint(auth_bp, url_prefix=URL_PREFIX)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
