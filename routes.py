
import datetime
import bcrypt
from flask import send_from_directory, render_template, session, redirect, url_for, request
from app import app
from validation import userSchema, changingPasswordSchema, changingEmailSchema, changingUserDataSchema, voteSchema
from marshmallow import ValidationError
from database.models import User, Vote, VoteOption, Voting
from database.models import db


# endpoints

@app.route("/")
def main_page():
    id = session.get("idUser")
    if id:
        statusFilter = request.args.get("statusFilter", 'In progress')
        titleFilter = request.args.get("titleFilter", '')
        startDateFilter = request.args.get("startDateFilter", '')
        endDateFilter = request.args.get("endDateFilter", '')
        votes = db.session.query(Vote).filter(Vote.title.like(f"%{titleFilter}%"))
        if startDateFilter:
            votes = votes.filter(Vote.startDate <= startDateFilter)
        if endDateFilter:
            votes = votes.filter(Vote.endDate >= endDateFilter)
        votes = votes.all()
        votes = [vote.to_dict() for vote in votes]
        if statusFilter:
            votes = [vote for vote in votes if vote["status"] == statusFilter]
        return render_template("pages/main.html", votes=votes)
    else:
        return redirect(url_for("welcome_page"))


@app.route("/voting/<idVote>", methods=["GET", "POST"])
def voting(idVote):
    id = session.get("idUser")
    if id:
        user = db.session.query(User).filter(User.id == id).first()
        vote = db.session.query(Vote).filter(Vote.id == idVote).first()
        alreadyVoted = any(any(voting.idVoteOption == option.id for option in vote.options) for voting in user.votings)
        if not (alreadyVoted or vote.endDate <= datetime.datetime.today() or vote.startDate > datetime.datetime.today()):
            if request.method == "POST":
                data = request.form.to_dict()
                chosenOption = data.get("voteOption")
                voting = Voting(
                    idVoteOption=chosenOption,
                    idUser=id
                )
                db.session.add(voting)
                db.session.commit()
                return redirect(url_for("preview", idVote=idVote))
            else:
                # displaying vote options
                return render_template("forms/voting.html", vote=vote)
        else:
            return redirect(url_for("preview", idVote=idVote))
    else:
        return redirect(url_for("welcome_page"))

@app.route("/preview/<idVote>", methods=["GET", "POST"])
def preview(idVote):
    id = session.get("idUser")
    if id:
        vote = db.session.query(Vote).filter(Vote.id == idVote).first()
        user = db.session.query(User).filter(User.id == id).first()
        if request.method == "POST":
            pass
        else:
            originPage = request.args.get("originPage", "votes_page")
            alreadyVoted = any(any(voting.idVoteOption == option.id for option in vote.options) for voting in user.votings)
            return render_template("pages/preview.html", vote=vote.to_dict(), user=vote.user.to_dict(), originPage=originPage, alreadyVoted=alreadyVoted)
    else:
        return redirect(url_for("welcome_page"))

@app.route("/votes")
def votes_page():
    id = session.get("idUser")
    if id:
        statusFilter = request.args.get("status")
        titleFilter = request.args.get("titleFilter", '')
        success = request.args.get("successMessage")
        votes = db.session.query(Vote).filter(Vote.idUser == id).filter(Vote.title.like(f"%{titleFilter}%")).all()
        votes = [vote.to_dict() for vote in votes] if len(votes) > 0 else None
        if statusFilter:
            votes = [vote for vote in votes if vote["status"] == statusFilter]
        return render_template("pages/votes.html", votes=votes, success=success)
    else:
        return redirect(url_for("welcome_page"))
    

@app.route("/deleting_vote", methods=["GET", "POST"])
def deleting_vote():
    id = session.get("idUser")
    if id:
        idVote = request.args.get("idVote")
        ownership = db.session.query(Vote).filter(Vote.id == idVote).filter(Vote.idUser == id).count()
        if request.method == "POST":
            if ownership == 1:
                vote = db.session.query(Vote).filter(Vote.id == idVote).first()
                db.session.delete(vote)
                db.session.commit()
                return redirect(url_for("votes_page", successMessage="Vote deleted successfully"))
            else:
                return redirect(url_for("votes_page"))
        else:
            return render_template("confirms/delete.html", forbidden=ownership == 0)
    else:
        return redirect(url_for("welcome_page"))


@app.route("/creating_vote", methods=["GET", "POST"])
def creating_vote():
    id = session.get("idUser")
    if id:
        count = request.args.get("count")
        if count:
            if request.method == "POST":
                # creating vote
                data = request.form.to_dict()
                voteOptions = request.form.getlist("voteOptions")
                data["voteOptions"] = voteOptions
                data["realTimeResults"] = "realTimeResults" in data
                try:
                    voteSchema.load(data)
                except ValidationError as err:
                    data["count"] = int(count)
                    return render_template("forms/creatingVote.html", errors=err.messages, values=data)
                vote = Vote(
                    title=data.get("voteTitle"),
                    startDate=data.get("startDate"),
                    endDate=data.get("endDate"),
                    description=data.get("description"),
                    realTimeResults=data.get("realTimeResults"),
                    idUser=id
                )
                voteOptions=[
                    VoteOption(idVote=vote.id, name=name) for name in voteOptions
                ]
                vote.options = voteOptions
                db.session.add(vote)
                db.session.commit()
                return redirect(url_for("votes_page", successMessage="Created new Vote"))
            else:
                return render_template("forms/creatingVote.html", values={"count":int(count)})
        else:
            return render_template("forms/creatingVote.html", values={})
    else:
        return redirect(url_for("welcome_page"))



@app.route("/welcome")
def welcome_page():
    return render_template("pages/landingPage.html")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        data = request.form.to_dict()
        try:
            userSchema.load(data)
        except ValidationError as err:
            return render_template("forms/register.html", errors=err.messages, values=data)
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
            except ValidationError as err:
                return render_template("forms/changePassword.html", errors=err.messages, values=data)
            # valid data
            passwordBytes = str(data.get("password")).encode("utf-8")
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(passwordBytes, salt)
            db.session.query(User).filter(User.id == id).update({User.password: hash.decode()})
            db.session.commit()
            user = db.session.query(User).filter(User.id == id).first()
            return render_template("pages/user.html", found=True, permission=user.id == id, user=user, success="Changing password success")
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
            except ValidationError as err:
                return render_template("forms/changeEmail.html", errors=err.messages, values=data)
            if(db.session.query(User).filter(User.email == data.get("email")).count() > 0):
                return render_template("forms/changeEmail.html", errors={"email":["This email is already taken"]}, values=data)
            db.session.query(User).filter(User.id == id).update({User.email: data.get("email")})
            db.session.commit()
            user = db.session.query(User).filter(User.id == id).first()
            return render_template("pages/user.html", found=True, permission=user.id == id, user=user, success="Changing email success")
        else:
            user = db.session.query(User).filter(User.id == id).first()
            return render_template("forms/changeEmail.html", values={"email":user.email})
    else:
        return redirect(url_for("main_page"))
    
@app.route("/changing_data", methods=["GET", "POST"])
def changing_data():
    id = session.get("idUser")
    if id:
        if request.method == "POST":
            data = request.form.to_dict()
            try:
                changingUserDataSchema.load(data)
            except ValidationError as err:
                return render_template("forms/changeData.html", errors=err.messages, values=data)
            db.session.query(User).filter(User.id == id).update({User.name: data.get("name"), User.surname: data.get("surname")})
            db.session.commit()
            user = db.session.query(User).filter(User.id == id).first()
            return render_template("pages/user.html", found=True, permission=user.id == id, user=user, success="Changing name & surname success")
        else:
            user = db.session.query(User).filter(User.id == id).first()
            return render_template("forms/changeData.html", values={"name":user.name, "surname":user.surname})
    else:
        return redirect(url_for("main_page"))
    
@app.route("/user/<id>", methods=["GET"])
def user_data(id):
    if session.get("idUser"):
        user = db.session.query(User).filter(User.id == id).first()
        if user:
            return render_template("pages/user.html", found=True, permission=session.get("idUser") == id, user=user)
        else:
            return render_template("pages/user.html", found=False)
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
    styleFile = request.args.get("styleFile", "index")
    return send_from_directory('styles', f"{styleFile}.css")