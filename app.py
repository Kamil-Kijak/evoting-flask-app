

import os
from flask import Flask
from dotenv import load_dotenv
load_dotenv()


# database
from models import db
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql://{os.getenv("DB_USER") or "root"}:{os.getenv("DB_PASSWORD") or ""}@{os.getenv("DB_HOST") or "localhost"}:{os.getenv("DB_PORT") or "root"}/{os.getenv("DB_NAME") or "evoting_flask_app_database"}'
db.init_app(app)
with app.app_context():
    db.create_all()

# endpoints

@app.route("/")
def mainPage():
    return "<h1>Hello world</h1>"


if __name__ == "__main__":
    app.run(debug=int(os.getenv("DEBUG")) or 0, port=os.getenv("PORT") or 3000)