
from flask import send_from_directory, render_template, session, redirect, url_for
from app import app

# endpoints

@app.route("/")
def mainPage():
    if not session.get("idUser"):
        return redirect(url_for("welcome_page"))
    return render_template("base.html")


@app.route("/welcome")
def welcome_page():
    return render_template("landingPage.html")

@app.route('/assets/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('assets', filename)

@app.route('/style')
def get_style():
    return send_from_directory('styles', "main.css")