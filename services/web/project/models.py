from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    classes = db.relationship('TeacherClasses', backref='teacher', lazy='dynamic')

    def __init__(self, email):
        self.email = email


# class Teacher(db.Model):
#     __tablename__ = 'teachers'
#
#     teacher_id = db.Column(db.Integer, primary_key=True)
#
#     password = db.Column(db.String(50), nullable=False)
#     role = db.Column(db.String(50), nullable=False)
#     school = db.Column(db.String(100), nullable=False)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False)
#     active = db.Column(db.Boolean(), default=True, nullable=False)
#     email = db.Column(db.String(128), db.ForeignKey('users.email'), nullable=False)
#
#     classes = db.relationship('teacher_classes', backref='teacher_id')


class TeacherClasses(db.Model):
    __tablename__ = 'teacher_classes'

    class_id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_name = db.Column(db.String(128), default=True, nullable=False)

    class_task = db.relationship('Task', backref='class_', lazy='dynamic')
    # class_no = db.relationship('class_members', backref='class_id')


class Task(db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key=True)

    task_name = db.Column(db.String(128), nullable=False)
    task_detail = db.Column(db.String(128), nullable=False)
    task_reason = db.Column(db.String(128), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('teacher_classes.class_id'), nullable=False)
    learn_id = db.Column(db.Integer, db.ForeignKey('learn.learn_id'), nullable=False)

class Learn(db.Model):
    __tablename__ = 'learn'

    learn_id = db.Column(db.Integer, primary_key=True)

    learn_title = db.Column(db.String(128), nullable=False)
    learn_detail = db.Column(db.String(128), nullable=False)

    tasks = db.relationship('Task', backref='learn', lazy='dynamic')
