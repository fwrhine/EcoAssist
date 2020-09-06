import string
import random
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
    return render_template("home.html")


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
            school = userDict['school']

            if username == reqUsername and password == reqPassword:
                print("login success")
                session['logged_in'] = True
                session['username'] = username
                session['first_name'] = first_name
                session['last_name'] = last_name
                session['role'] = role
                session['school'] = school
                return redirect(url_for('home'))
    return render_template("login.html", form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, role=session['role'], password=form.password.data,
                    first_name=form.first_name.data, last_name=form.last_name.data, school=form.school.data)
        db.session.add(user)
        db.session.commit()
        if session['role'] == 'teacher':
            print("add teacher to database")
            teacher = Teacher(email=form.email.data)
            db.session.add(teacher)
            db.session.commit()
            session['logged_in'] = True
            session['username'] = form.email.data
            session['first_name'] = form.first_name.data
            session['last_name'] = form.last_name.data
            session['school'] = form.school.data
        else:
            print("add student to database")
            student = Student(email=form.email.data)
            teacher_classes = TeacherClasses.query.filter_by(
                class_code=form.class_code.data).first()
            class_member = ClassMembers(
                class_=teacher_classes, student=student)
            db.session.add(student)
            db.session.add(class_member)
            db.session.commit()
            session['logged_in'] = True
            session['username'] = form.email.data
            session['first_name'] = form.first_name.data
            session['last_name'] = form.last_name.data
            session['school'] = form.school.data
        return redirect(url_for('home'))
    else:
        print("this")
    return render_template('register.html', form=form)


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

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)

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

    available_resource = Resource.query.all()
    resource_list = [(i.resource_id, i.resource_title)
                     for i in available_resource]

    form = TaskForm()
    form.resource_id.choices = resource_list
    form.class_id.choices = class_list

    if form.validate_on_submit():
        task = Task(task_name=form.title.data, task_detail=form.details.data, points=form.points.data,
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
            task_complete = TaskComplete.query.filter_by(
                student_id=student.student_id, task_id=i.task_id).first()
            if task_complete is not None:
                done = True
            else:
                done = False
        else:
            done = False

        tasks.append([i, class_name, done])

    print(tasks)

    return render_template('task_list.html', tasks=tasks)


@app.route('/task-completed', methods=['POST'])
def task_completed():
    task_id = request.form.get("task_id")
    student = Student.query.filter_by(email=session['username']).first()
    student_id = student.student_id

    existing = TaskComplete.query.filter_by(
        student_id=student_id, task_id=task_id).first()

    if existing is None:
        task_complete = TaskComplete(student_id=student_id, task_id=task_id)
        db.session.add(task_complete)
        status = "add"
    else:
        db.session.delete(existing)
        status = "delete"

    db.session.commit()
    return json.dumps({'status': status, 'task_id': task_id, 'student_id': student_id})


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


@app.route('/create-class', methods=['GET', 'POST'])
def create_class():
    form = ClassForm()

    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(email=session['username']).first()
        code = ''.join(random.choice(string.ascii_uppercase +
                                     string.digits) for _ in range(5))
        teacher_classes = TeacherClasses(
            class_name=form.class_name.data, class_code=code, teacher=teacher)
        db.session.add(teacher_classes)
        db.session.commit()
        return redirect(url_for('.class_list'))
    return render_template('create_class.html', form=form)

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    if session['role']=="student":
        student = Student.query.filter_by(email=session['username']).first()
        class_members = student.classes_student.first()

        # get teacher's name
        teacher_classes = TeacherClasses.query.filter_by(class_id=class_members.class_id).first()
        teacher = Teacher.query.filter_by(teacher_id=teacher_classes.teacher_id).first()
        teacher_user = User.query.filter_by(email=teacher.email).first()
        teacher_name = teacher_user.first_name + " " + teacher_user.last_name
        if teacher_name[-1] == 's':
            teacher_name = teacher_name + "'"
        else:
            teacher_name = teacher_name + "'s"

        # get all members of class
        all_members = ClassMembers.query.filter_by(class_id=class_members.class_id).all()
        leaderboard = {}

        # calculate points
        for i in all_members:
            points = 0
            all_task_completed = TaskComplete.query.filter_by(student_id=i.student_id).all()
            for j in all_task_completed:
                task = Task.query.filter_by(task_id=j.task_id).first()
                points += task.points

            current_student = Student.query.filter_by(student_id=i.student_id).first()
            current_user = User.query.filter_by(email=current_student.email).first()
            name = current_user.first_name + " " + current_user.last_name
            new = {i.student_id:(name, points)}
            # key being student_id instead of name is intentional
            leaderboard.update(new)

        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1][1], reverse=True)
        return render_template('student_leaderboard.html', leaderboard=sorted_leaderboard,
        teacher=teacher_name, class_name=teacher_classes.class_name)
    else:
        teacher = Teacher.query.filter_by(email=session['username']).first()
        class_list = teacher.classes.all()
        leaderboard = {}

        # calculate points
        for i in class_list:
            points = 0
            all_members = ClassMembers.query.filter_by(class_id=i.class_id).all()
            for j in all_members:
                all_task_completed = TaskComplete.query.filter_by(student_id=j.student_id).all()
                for k in all_task_completed:
                    task = Task.query.filter_by(task_id=k.task_id).first()
                    points += task.points
            new = {i.class_id:(i.class_name, points)}
            # key being class_id instead of name is intentional
            leaderboard.update(new)

        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1][1], reverse=True)
        return render_template('teacher_leaderboard.html',leaderboard=sorted_leaderboard)

@app.route("/profile")
def profile():
    if (session['role'] == "teacher"):
        teacher = Teacher.query.filter_by(email=session['username']).first()
        class_list = teacher.classes.all()
        return render_template('profile.html', email=session['username'], first_name=session['first_name'], last_name=session['last_name'],
                                    role="Teacher", school=session['school'], classes=class_list)
    else:
        if session['role']=="student":
            student = Student.query.filter_by(email=session['username']).first()
            print('student id : ' + str(student.student_id))
            class_members = student.classes_student.first()
            print(class_members.class_id)
            all_members = ClassMembers.query.filter_by(class_id=class_members.class_id).all()
            print(all_members)
            leaderboard = {}

            # get class name
            class_name = TeacherClasses.query.filter_by(class_id=class_members.class_id).first().class_name

            for i in all_members:
                points = 0
                all_task_completed = TaskComplete.query.filter_by(student_id=i.student_id).all()
                for j in all_task_completed:
                    task = Task.query.filter_by(task_id=j.task_id).first()
                    points += task.points
                print(points)
                new = {i.student_id:points}
                leaderboard.update(new)

            sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
            print('leaderboard : ' + str(leaderboard))

            rank = 1
            point = 0
            for j in sorted_leaderboard:
                id = int(j[0])
                if not (id == student.student_id):
                    rank += 1
                else:
                    point = j[1]
                    break

            return render_template('profile.html', email=session['username'],
                first_name=session['first_name'], last_name=session['last_name'],
                role="Student", school=session['school'], leaderboard=sorted_leaderboard,
                ranking=rank, total=len(leaderboard), points=point, class_name=class_name)
