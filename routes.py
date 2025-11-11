
import bcrypt
from flask import send_from_directory, render_template, session, redirect, url_for, request
from app import app
from validation import userSchema, changingPasswordSchema, changingEmailSchema
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
    
@app.route("/changing_password", methods=["GET", "POST"])
def changing_password():
    id = session.get("idUser")
    if id:
        if request.method == "POST":
            data = request.form.to_dict()
            try:
                changingPasswordSchema.load(data)
                # valid data
                passwordBytes = str(data.get("password")).encode("utf-8")
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(passwordBytes, salt)
                db.session.query(User).filter(User.id == id).update({User.password: hash.decode()})
                db.session.commit()
                user = db.session.query(User).filter(User.id == id).first()
                return render_template("user.html", found=True, permission=user.id == id, user=user, success="Changing password success")
            except ValidationError as err:
                return render_template("forms/changePassword.html", errors=err.messages, values=data)
        else:
            return render_template("forms/changePassword.html", values={})
    else:
        return redirect(url_for("main_page"))
    
@app.route("/changing_email", methods=["GET", "POST"])
def changing_email():
    id = session.get("idUser")
    if id:
        if request.method == "POST":
            data = request.form.to_dict()
            try:
                changingEmailSchema.load(data)
                if(db.session.query(User).filter(User.email == data.get("email")).count() > 0):
                    return render_template("forms/changeEmail.html", errors={"email":["This email is already taken"]}, values=data)
                db.session.query(User).filter(User.id == id).update({User.email: data.get("email")})
                db.session.commit()
                user = db.session.query(User).filter(User.id == id).first()
                return render_template("user.html", found=True, permission=user.id == id, user=user, success="Changing email success")
            except ValidationError as err:
                return render_template("forms/changeEmail.html", errors=err.messages, values=data)
        else:
            user = db.session.query(User).filter(User.id == id).first()
            return render_template("forms/changeEmail.html", values={"email":user.email})
    else:
        return redirect(url_for("main_page"))
    
@app.route("/user/<id>", methods=["GET"])
def user_data(id):
    if session.get("idUser"):
        user = db.session.query(User).filter(User.id == id).first()
        if user:
            return render_template("user.html", found=True, permission=user.id == id, user=user)
        else:
            return render_template("user.html", found=False)
    else:
        return redirect(url_for("main_page"))

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