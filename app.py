

import os
import secrets
from flask import Flask
from dotenv import load_dotenv
load_dotenv()


# database
from database.models import db
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{os.getenv("DB_USER") or "root"}:{os.getenv("DB_PASSWORD") or ""}@{os.getenv("DB_HOST") or "localhost"}:{os.getenv("DB_PORT") or "root"}/{os.getenv("DB_NAME") or "evoting_flask_app_database"}'
# app.config["SECRET_KEY"] = secrets.token_hex(32)
app.config["SECRET_KEY"] = "7b62e655f1c8db498ea1fe56ee1deed2cee0e7ca9a6da2a79f7da0aab0379a1a"
db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    from routes import *
    app.run(debug=int(os.getenv("DEBUG")) or 0, port=os.getenv("PORT") or 3000)