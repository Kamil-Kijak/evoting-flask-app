

import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def mainPage():
    return "<h1>Hello world</h1>"


if __name__ == "__main__":
    app.run(debug=int(os.getenv("DEBUG")) or 0, port=os.getenv("PORT") or 3000)