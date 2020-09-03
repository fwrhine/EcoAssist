import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    json,
    redirect,
    url_for,
    flash,
    render_template,
    session
)
from flask_sqlalchemy import SQLAlchemy
from .models import *
from .forms import *


app = Flask(__name__)
app.config.from_object("project.config.Config")
db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def home():
    return render_template("home.html", session=session)

@app.route("/login",  methods=['POST', 'GET'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        reqUsername = form.email.data
        reqPassword = form.password.data

        user = db.session.execute('select * from users')
        for i in user:
            userDict = dict(i)
            username = userDict['email']
            first_name = userDict['first_name']
            last_name = userDict['last_name']
            role = userDict['role']
            password = userDict['password']

            if username == reqUsername and password == reqPassword:
                print("login success")
                session['logged_in'] = True
                session['username'] = username
                session['first_name'] = first_name
                session['last_name'] = last_name
                session['role'] = role
                return redirect(url_for('home'))
    return render_template("login.html", form = form)


@app.route('/register',methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, role=session['role'], password=form.password.data, first_name=form.first_name.data, last_name=form.last_name.data, school=form.school.data)
        db.session.add(user)
        db.session.commit()
        if session['role'] == 'teacher':
            print("add teacher to database")
            teacher = Teacher(email=form.email.data)
            db.session.add(teacher)
            db.session.commit()
        else:
            print("add student to database")
            student = Student(email=form.email.data)
            teacher_classes = TeacherClasses.query.filter_by(class_code=form.class_code.data).first()
            class_member = ClassMembers(class_=teacher_classes, student=student)
            db.session.add(student)
            db.session.add(class_member)
            db.session.commit()

        return redirect(url_for('home'))
    return render_template('register.html', form = form)

@app.route('/registerteacher', methods=['POST'])
def registerTeacher():
    session['role'] = 'teacher'
    return redirect(url_for('register'))

@app.route('/registerstudent', methods=['POST'])
def registerStudent():
    session['role'] = 'student'
    return redirect(url_for('register'))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return render_template("upload.html")


@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    teacher = Teacher.query.filter_by(email=session['username']).first()
    available_classes = teacher.classes.all()
    class_list = [(i.class_id, i.class_name) for i in available_classes]

    available_resource=Resource.query.all()
    resource_list=[(i.resource_id, i.resource_title) for i in available_resource]

    form = TaskForm()
    form.resource_id.choices = resource_list
    form.class_id.choices = class_list

    if form.validate_on_submit():
        task = Task(task_name=form.title.data, task_detail=form.details.data,
        task_reason=form.reason.data, points=form.points.data,
        class_id=form.class_id.data, resource_id=form.resource_id.data, teacher=teacher)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('.task_list'))
    return render_template('create_task.html', form=form)

@app.route("/task-list")
def task_list():
    if session['role'] == "student":
        student = Student.query.filter_by(email=session['username']).first()
        class_members = student.classes_student.first()
        teacher_classes = TeacherClasses.query.get(class_members.class_id)
        task_list = teacher_classes.class_task.all()
    else:
        teacher = Teacher.query.filter_by(email=session['username']).first()
        task_list = teacher.tasks.all()

    tasks = []

    for i in task_list:
        teacher_classes = TeacherClasses.query.get(i.class_id)
        class_name = teacher_classes.class_name

        if session['role'] == "student":
            task_complete = TaskComplete.query.filter_by(student_id=student.student_id, task_id=i.task_id).first()
            if task_complete is not None:
                done = True
            else:
                done = False
        else:
            done = False

        tasks.append([i, class_name, done])

    print(tasks)

    return render_template('task_list.html', tasks=tasks, session=session)

@app.route('/task-completed', methods=['POST'])
def task_completed():
    task_id = request.form.get("task_id")
    student = Student.query.filter_by(email=session['username']).first()
    student_id = student.student_id

    existing = TaskComplete.query.filter_by(student_id=student_id, task_id=task_id).first()

    if existing is None:
        task_complete = TaskComplete(student_id=student_id, task_id=task_id)
        db.session.add(task_complete)
        status = "add"
    else:
        db.session.delete(existing)
        status = "delete"

    db.session.commit()
    return json.dumps({'status':status,'task_id':task_id, 'student_id':student_id})

@app.route("/learn")
def learn():
    resource_list = Resource.query.all()
    print(resource_list)
    return render_template('learn.html', resource_list=resource_list)

@app.route("/learn/<id>")
def resource_details(id):
    resource = Resource.query.get(id)
    return render_template('learn_details.html', learn=resource)

@app.route("/class")
def class_list():
    teacher = Teacher.query.filter_by(email=session['username']).first()
    class_list = teacher.classes.all()
    return render_template('class_list.html', class_list=class_list)

import random, string
@app.route('/create-class', methods=['GET', 'POST'])
def create_class():
    form = ClassForm()

    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(email=session['username']).first()
        code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        teacher_classes = TeacherClasses(class_name=form.class_name.data, class_code=code, teacher=teacher)
        db.session.add(teacher_classes)
        db.session.commit()
        return redirect(url_for('.class_list'))
    return render_template('create_class.html', form=form)
