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
from .models import db, User, Task
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


@app.route('/new-task', methods=['GET', 'POST'])
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, details=form.details.data,
        reason=form.reason.data, points=form.points.data)
        db.session.add(task)
        db.session.commit()
        # get_task = Task.query.get(1)
        # flash('Task {} created'.format(form.title.data))
        # flash('Task {} created'.format(get_task.title))
        return redirect(url_for('.task_list'))
    return render_template('new_task.html', form=form)

@app.route("/task-list")
def task_list():
    tasks = Task.query.all()
    return render_template('task_list.html', tasks=tasks)

@app.route('/task-completed', methods=['POST'])
def task_completed():
    id = request.form.get("task_id")
    return json.dumps({'status':'OK','task_id':id})
