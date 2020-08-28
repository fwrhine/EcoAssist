from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10),nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(10),nullable=False)
    last_name = db.Column(db.String(10),nullable=False)
    password = db.Column(db.String(128), nullable=False)
    school = db.Column(db.String(128), nullable=False)

    def __init__(self, role, email, first_name, last_name, password, school):
        self.role = role
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.school = school

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
