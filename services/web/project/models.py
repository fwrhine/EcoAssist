from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(128), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    teacher_email = db.relationship(
        'Teacher', backref='teacher', lazy='dynamic')
    student_email = db.relationship(
        'Student', backref='student', lazy='dynamic')

    def set_password(self, password):
        '''
        Set user password with generated hash.
        '''
        self.password = generate_password_hash(password)

    def check_password(self, password):
        '''
        Check if password matches hashed password.
        '''
        return check_password_hash(self.password, password)

class Teacher(db.Model):
    __tablename__ = 'teachers'

    teacher_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), db.ForeignKey(
        'users.email'), nullable=False)

    classes = db.relationship(
        'TeacherClasses', backref='teacher', lazy='dynamic')
    tasks = db.relationship('Task', backref='teacher', lazy='dynamic')


class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), db.ForeignKey(
        'users.email'), nullable=False)

    classes_student = db.relationship(
        'ClassMembers', backref='student', lazy='dynamic')
    student_task_done = db.relationship(
        'TaskComplete', backref='student', lazy='dynamic')


class TeacherClasses(db.Model):
    '''
    Table for all classes with foreign key to associated teacher.
    '''
    __tablename__ = 'teacher_classes'

    class_id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'teachers.teacher_id'), nullable=False)
    class_name = db.Column(db.String(128), default=True, nullable=False)
    class_code = db.Column(db.String(128), default=True, nullable=False)

    class_no = db.relationship(
        'ClassMembers', backref='class_', lazy='dynamic')
    class_task = db.relationship('Task', backref='class_', lazy='dynamic')


class ClassMembers(db.Model):
    '''
    Table for one-to-many relationship between classes
    and the members of the class.
    '''
    __tablename__ = 'class_members'

    class_member_id = db.Column(db.Integer, primary_key=True)

    # Student status: approved, pending, or rejected by teacher
    student_status = db.Column(db.String(50), nullable=False)

    class_id = db.Column(db.Integer, db.ForeignKey(
        'teacher_classes.class_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'students.student_id'), nullable=False)


class Task(db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key=True)

    task_name = db.Column(db.String(128), nullable=False)
    task_detail = db.Column(db.String(), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey(
        'teacher_classes.class_id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'teachers.teacher_id'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey(
        'resource.resource_id'), nullable=False)
    required_approval = db.Column(db.Boolean, nullable=False)

    task_done = db.relationship('TaskComplete', backref='task', lazy='dynamic')


class TaskComplete(db.Model):
    '''
    Table for many-to-many relationship between tasks and students.
    Stores task status of individual students.
    '''
    __tablename__ = 'task_complete'

    task_complete_id = db.Column(db.Integer, primary_key=True)

    # Task status: completed, incomplete, accepted, or rejected.
    task_status = db.Column(db.String(50), nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey(
        'students.student_id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey(
        'task.task_id'), nullable=False)


class Resource(db.Model):
    __tablename__ = 'resource'

    resource_id = db.Column(db.Integer, primary_key=True)

    resource_title = db.Column(db.String(128), nullable=False)
    resource_detail = db.Column(db.String(128), nullable=False)

    tasks = db.relationship('Task', backref='resource', lazy='dynamic')


class Badge(db.Model):
    __tablename__ = 'badges'

    badge_no = db.Column(db.Integer, primary_key=True)
    badge_name = db.Column(db.String(128), nullable=False)
    badge_comment = db.Column(db.String(), nullable=False)
    badge_location = db.Column(db.String(128), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'students.student_id'), nullable=False)
