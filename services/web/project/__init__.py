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
    render_template
)
from flask_sqlalchemy import SQLAlchemy
from .models import db, User, TeacherClasses, Task, Learn
from .forms import TaskForm


app = Flask(__name__)
app.config.from_object("project.config.Config")
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


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
    available_classes=db.session.query(TeacherClasses).filter(TeacherClasses.teacher_id == 1).all()
    #Now forming the list of tuples for SelectField
    class_list=[(i.class_id, i.class_name) for i in available_classes]
    form = TaskForm()
    form.class_id.choices = class_list
    if form.validate_on_submit():
        task = Task(task_name=form.title.data, task_detail=form.details.data,
        task_reason=form.reason.data, points=form.points.data, class_id=form.class_id.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('.task_list'))
    return render_template('new_task.html', form=form)

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
