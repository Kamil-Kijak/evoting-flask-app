
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, date
from nanoid import generate

# creating database first
from . import creatingDatabase

db = SQLAlchemy()

nowUtc = datetime.now(timezone.utc)

def generateNanoId() -> str:
    return generate()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(21), primary_key=True, default=generateNanoId)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    votes = db.relationship('Vote', backref='user', lazy=True, passive_deletes=True)

    def __repr__(self):
        return f"<User {self.email}>"
    
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "surname":self.surname,
            "email":self.email,
            "votes":[vote.to_dict() for vote in self.votes],
        }

class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column(db.String(21), primary_key=True, default=generateNanoId)
    title = db.Column(db.String(50))
    startDate = db.Column(db.DateTime, default=nowUtc, nullable=False)
    endDate = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.Text, nullable=False)
    realTimeResults = db.Column(db.Boolean, default=True, nullable=False)
    options = db.relationship('VoteOption', backref='vote', lazy=True, passive_deletes=True)
    idUser = db.Column(db.String(21), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<Vote {self.title}>"
    
    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "startDate":self.startDate.strftime("%d.%m.%Y"),
            "endDate":self.endDate.strftime("%d.%m.%Y"),
            "description":self.description,
            "realTimeResults":self.realTimeResults,
            "options":[option.to_dict() for option in self.options],
            "idUser":self.idUser,
            "status":"Waiting" if self.startDate > datetime.today() else "Ended" if self.endDate < datetime.today() else "In progress"
        }
    
class VoteOption(db.Model):
    __tablename__ = 'voteOption'
    id = db.Column(db.String(21), primary_key=True, default=generateNanoId)
    idVote = db.Column(db.String(21), db.ForeignKey('vote.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    votings = db.relationship('Voting', backref='voteOption', lazy=True, passive_deletes=True)

    def __repr__(self):
        return f"<VoteOption {self.name}>"
    
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "votingCount":len(self.votings)
        }

class Voting(db.Model):
    __tablename__ = 'voting'
    id = db.Column(db.String(21), primary_key=True, default=generateNanoId)
    idUser = db.Column(db.String(21), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    idVoteOption = db.Column(db.String(21), db.ForeignKey('voteOption.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<Voting {self.id}>"