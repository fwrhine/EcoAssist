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
def index():
    return render_template("index.html")

@app.route("/login",  methods=['POST', 'GET'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        reqUsername = form.email.data
        print(reqUsername)
        reqPassword = form.password.data
        print(reqPassword)

        user = db.session.execute('select * from users')
        for i in user:
            userDict = dict(i)
            name = userDict['email']
            passw = userDict['password']
            print(name+passw)

            if name == reqUsername and passw == reqPassword:
                print("suc")
                session['logged_in'] = True
                session['username'] = name
                return homePage()
    return render_template("login.html", form = form)


@app.route('/register',methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("yeay")
        user = User(email=form.email.data, role=session['role'], password=form.password.data, first_name=form.first_name.data, last_name=form.last_name.data, school=form.school.data)
        db.session.add(user)
        db.session.commit()
        if session['role'] == 'teacher':
            teacher = Teacher(email=form.email.data)
            db.session.add(teacher)
            db.session.commit()
        else:
            student = Student(email=form.email.data)
            db.session.add(student)
            db.session.commit()

        session['username'] = form.email.data
        session['logged_in'] = True
        print("suk")
        return redirect(url_for('homePage'))
    print("fail")
    return render_template('register.html', form = form)

@app.route('/registerteacher', methods=['POST'])
def registerTeacher():
    session['role'] = 'teacher'
    return redirect(url_for('register'))

@app.route('/registerstudent', methods=['POST'])
def registerStudent():
    session['role'] = 'student'
    return redirect(url_for('register'))

@app.route('/homepage',methods=['POST', 'GET'])
def homePage():
    name = session['username']
    return render_template('main.html', name = name)

@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    session['logged_in'] = False
    return index()


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return render_template("upload.html")


@app.route('/create-task', methods=['GET', 'POST'])
def create_task():
    available_classes=db.session.query(TeacherClasses).filter(TeacherClasses.teacher_id == 1).all()
    class_list=[(i.class_id, i.class_name) for i in available_classes]

    available_learn=Learn.query.all()
    learn_list=[(i.learn_id, i.learn_title) for i in available_learn]

    form = TaskForm()
    form.learn_id.choices = learn_list
    form.class_id.choices = class_list

    if form.validate_on_submit():
        task = Task(task_name=form.title.data, task_detail=form.details.data,
        task_reason=form.reason.data, points=form.points.data, class_id=form.class_id.data, learn_id=form.learn_id.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('.task_list'))
    return render_template('create_task.html', form=form)

@app.route("/task-list")
def task_list():
    class_ = TeacherClasses.query.get(1)
    tasks = class_.class_task.all()
    return render_template('task_list.html', tasks=tasks)

@app.route('/task-completed', methods=['POST'])
def task_completed():
    id = request.form.get("task_id")
    return json.dumps({'status':'OK','task_id':id})

@app.route("/learn")
def learn():
    learn_list = Learn.query.all()
    return render_template('learn.html', learn_list=learn_list)

@app.route("/learn/<id>")
def learn_details(id):
    learn = Learn.query.get(id)
    return render_template('learn_details.html', learn=learn)
