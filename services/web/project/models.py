from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    details = db.Column(db.String(128))
    reason = db.Column(db.String(128))
    points = db.Column(db.Integer)

    def __init__(self, title, details, reason, points):
        self.title = name;
        self.details = details;
        self.reason = reason;
        self.points = points;
