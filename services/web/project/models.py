from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    teacher_email = db.relationship('teachers', backref='teacher_email')
    student_email = db.relationship('students', backref='student_email')

    def __init__(self, email):
        self.email = email


# class Person(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     addresses = db.relationship('Address', backref='person', lazy=True)
#
# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
#         nullable=False)

class Teacher(db.Model):
    __tablename__ = 'teachers'

    teacher_id = db.Column(db.Integer, primary_key=True)

    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    email = db.Column(db.String(128), db.ForeignKey('users.email'), nullable=False)

    classes = db.relationship('teacher_classes', backref='teacher_id')


class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)

    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    email = db.Column(db.String(128), db.ForeignKey('users.email'), nullable=False)

    classes_student = db.relationship('class_members', backref='student_id')
    student_task_done = db.relationship('TaskComplete', backref='student_id')
    student_points = db.relationship('points', backref='student_id')


class TeacherClasses(db.Model):
    __tablename__ = 'teacher_classes'

    class_id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=False)
    class_name = db.Column(db.String(128), default=True, nullable=False)

    class_no = db.relationship('class_members', backref='class_id')


class ClassMembers(db.Model):
    __tablename__ = 'class_members'

    class_member_id = db.Column(db.Integer, primary_key=True)

    class_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)

    class_task = db.relationship('task', backref='class_id')


class Task(db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key=True)

    task_name = db.Column(db.String(128), nullable=False)
    task_detail = db.Column(db.String(128), nullable=False)
    task_reason = db.Column(db.String(128), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class_members.class_member_id'), nullable=False)

    task_done = db.relationship('task_complete', backref='task_done')


class TaskComplete(db.Model):
    __tablename__ = 'task_complete'

    task_complete_id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'), nullable=False)


class Points(db.Model):
    __tablename__ = 'points'

    point_id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime, nullable=False)
    points = db.Column(db.Integer,  nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)



