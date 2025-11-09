
import bcrypt
from flask import send_from_directory, render_template, session, redirect, url_for, request
from app import app
from validation import userSchema
from marshmallow import ValidationError
from database.models import User
from database.models import db


# endpoints

@app.route("/")
def main_page():
    if not session.get("idUser"):
        return redirect(url_for("welcome_page"))
    return render_template("main.html")


@app.route("/welcome")
def welcome_page():
    return render_template("landingPage.html")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            userSchema.load(data)
            # success
            if(db.session.query(User).filter(User.email == data.get("email")).count() > 0):
                return render_template("forms/register.html", errors={"email":["This email is already taken"]}, values=data)
            passwordBytes = str(data.get("password")).encode("utf-8")
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(passwordBytes, salt)
            newUser = User(
                name=data.get("name").capitalize(),
                surname=data.get("surname").capitalize(),
                email=data.get("email"),
                password=hash.decode()
            )
            db.session.add(newUser)
            db.session.commit()
            session["idUser"] = newUser.id
            return redirect(url_for("main_page"))
        except ValidationError as err:
            return render_template("forms/register.html", errors=err.messages, values=data)

    else:
        return render_template("forms/register.html", values={})

@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        data = request.form.to_dict()
        if db.session.query(User).filter(User.email == data.get("email")).count() == 0:
            return render_template("forms/login.html", errors={"email":["User with this email doesn't exist"]}, values=data)
        user = db.session.query(User).filter(User.email == data.get("email")).first()
        if bcrypt.checkpw(str(data.get("password")).encode(), str(user.password).encode()):
            # login successfully
            session["idUser"] = user.id
            return redirect(url_for("main_page"))
        else:
            return render_template("forms/login.html", errors={"password":["Invalid password"]}, values=data)
    else:
        return render_template("forms/login.html", values={})
    
@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for("main_page"))

@app.route('/assets/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('assets', filename)

@app.route('/style')
def get_style():
    return send_from_directory('styles', "main.css")