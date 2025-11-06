import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from nanoid import generate
import pymysql

# creating database first

connection = pymysql.connect(
    host=os.getenv("DB_HOST") or "localhost",
    user=os.getenv("DB_USER") or "root",
    password=os.getenv("DB_PASSWORD") or "root"
)

with connection.cursor() as cursor:
    try:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {os.getenv("DB_NAME") or "evoting_flask_app_database"} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;')
        print("Database creation succeed")
    except pymysql.MySQLError as e:
        print("Database creation failed")

pymysql.install_as_MySQLdb()
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

    def __repr__(self):
        return f"<User {self.email}>"

class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column(db.String(21), primary_key=True, default=generateNanoId)
    title = db.Column(db.String(50))
    startDate = db.Column(db.DateTime, default=nowUtc, nullable=False)
    endDate = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.Text, nullable=False)
    realTimeResults = db.Column(db.Boolean, default=True, nullable=False)
    options = db.relationship('voteOption', backref='vote', lazy=True)

    def __repr__(self):
        return f"<Vote {self.title}>"
    
class VoteOption(db.Model):
    __tablename__ = 'voteOption'
    id = db.Column(db.String(21), primary_key=True, default=generateNanoId)
    idVote = db.Column(db.String(21), db.ForeignKey('vote.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<VoteOption {self.name}>"

class Voting(db.Model):
    __tablename__ = 'voting'
    id = db.Column(db.String(21), primary_key=True, default=generateNanoId)
    idUser = db.Column(db.String(21), db.ForeignKey('user.id'), nullable=False)
    idVoteOption = db.Column(db.String(21), db.ForeignKey('voteOption.id'), nullable=False)

    def __repr__(self):
        return f"<Voting {self.id}>"