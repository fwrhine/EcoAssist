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

# Key for development only
app.secret_key = "development-key"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login",  methods=['POST', 'GET'])
def loginPage():
    '''
    Renders the login page.
    On login success, redirects to page according to user's role and status.
    '''
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Set sessions
        session['logged_in'] = True
        session['username'] = user.email
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        session['role'] = user.role
        session['school'] = user.school

        if session['role'] == 'student':
            student = Student.query.filter_by(email=user.email).first()
            class_members = student.classes_student.first()
            if class_members:
                if class_members.student_status == "accepted":
                    return redirect(url_for('home'))
                else:
                    '''
                    If student has not been accepted by teacher,
                    display only the profile page without access to other pages.
                    '''
                    return redirect(url_for('.profile'))
            else:
                return redirect(url_for('.profile'))
            session['status'] = class_members.student_status

        return redirect(url_for('home'))

    return render_template("login.html", form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    '''
    Renders the register page.
    On form submission, adds user to database and redirects to
    page according to user's role and status.
    '''
    form = RegisterForm()
    if form.validate_on_submit():
        # Add user to database
        user = User(email=form.email.data, role=session['role'],
                    first_name=form.first_name.data, last_name=form.last_name.data, school=form.school.data)

        # Password hashing
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        # Set sessions
        session['logged_in'] = True
        session['username'] = form.email.data
        session['first_name'] = form.first_name.data
        session['last_name'] = form.last_name.data
        session['school'] = form.school.data

        if session['role'] == 'teacher':
            teacher = Teacher(email=form.email.data)
            db.session.add(teacher)
            db.session.commit()
        else:
            student = Student(email=form.email.data)

            if form.class_code.data:
                # Add student to class
                teacher_classes = TeacherClasses.query.filter_by(
                    class_code=form.class_code.data).first()
                class_member = ClassMembers(
                    class_=teacher_classes, student=student, student_status="pending")

                session['status'] = "pending"

                db.session.add(class_member)
                db.session.add(student)
                db.session.commit()
                '''
                When student has not been accepted by teacher,
                display only the profile page without access to other pages.
                '''
                return redirect(url_for('.profile'))

            else:
                db.session.add(student)
                db.session.commit()
                '''
                When student has not entered a class code,
                display only the profile page without access to other pages.
                '''
                return redirect(url_for('.profile'))

        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/registerteacher', methods=['POST'])
def registerTeacher():
    '''
    A register route for teachers.
    Sets session role to 'teacher' and redirects to register page.
    '''
    session['role'] = 'teacher'
    return redirect(url_for('register'))


@app.route('/registerstudent', methods=['POST'])
def registerStudent():
    '''
    A register route for students.
    Sets session role to 'student' and redirects to register page.
    '''
    session['role'] = 'student'
    return redirect(url_for('register'))


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    '''
    Logs user out by clearing session.
    Redirects to home page.
    '''
    session.clear()
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.route("/static/<path:filename>")
def staticfiles(filename):
    '''
    Opens static files stored in static folder.
    '''
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    '''
    Opens static files stored in media folder.
    '''
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    '''
    Renders upload page.
    On file submission, saves file to media folder.
    '''
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return render_template("upload.html")


@app.route('/create-task', defaults={'id': None}, methods=['GET', 'POST'])
@app.route('/create-task/<id>', methods=['GET', 'POST'])
def create_task(id):
    '''
    Renders the create new task page.
    On form submission, adds the task to database and redirects to task list.
    '''
    teacher = Teacher.query.filter_by(email=session['username']).first()

    '''
    Query list of classes and learning resources to show in form.
    '''
    if id is None:
        '''
        If class id is not specified on url, lists all classes associated
        with logged in teacher.
        '''
        available_classes = teacher.classes.all()
        class_list = [(i.class_id, i.class_name) for i in available_classes]
    else:
        '''
        If class id is specified on url, list only the specified class.
        '''
        available_classes = TeacherClasses.query.filter_by(class_id=id).first()
        class_list = [(available_classes.class_id,
                       available_classes.class_name)]

    available_resource = Resource.query.all()
    resource_list = [(i.resource_id, i.resource_title)
                     for i in available_resource]

    form = TaskForm()
    form.resource_id.choices = resource_list
    form.class_id.choices = class_list

    if form.validate_on_submit():
        '''
        On form submission, adds the task to database and redirects to
        the task list of the class the task is assigned to.
        '''
        task = Task(task_name=form.title.data, task_detail=form.details.data, points=form.points.data,
                    class_id=form.class_id.data, resource_id=form.resource_id.data, teacher=teacher,
                    required_approval=form.required_approval.data)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('.task_list', id=form.class_id.data))
    return render_template('create_task.html', form=form)


@app.route('/task-list', defaults={'id': None})
@app.route('/task-list/<id>')
def task_list(id):
    '''
    Renders the task list page.
    Queries task to be shown according to user's role.
    '''
    class_name = "" # Class name to be passed to template if role is teacher

    # Query list of tasks according to role
    if session['role'] == "student":
        student = Student.query.filter_by(email=session['username']).first()
        class_members = student.classes_student.first()
        teacher_classes = TeacherClasses.query.get(class_members.class_id)
        task_list = teacher_classes.class_task.all()
    else:
        teacher = Teacher.query.filter_by(email=session['username']).first()
        task_list = teacher.tasks.filter_by(class_id=id)
        class_name = TeacherClasses.query.filter_by(
            class_id=id).first().class_name

    tasks = []

    '''
    Appends task status to list of tasks.
    '''
    for i in task_list:
        teacher_classes = TeacherClasses.query.get(i.class_id)

        if session['role'] == "student":
            task_complete = TaskComplete.query.filter_by(
                student_id=student.student_id, task_id=i.task_id).first()
            status = ""
            if task_complete is not None:
                done = True
                status = task_complete.task_status
            else:
                done = False
        else:
            # If role is teacher, append empty status.
            status = ""
            done = False

        tasks.append([i, done, status])

    tasks.reverse() # Reverse list of task so the most recently created task is shown first.
    return render_template('task_list.html', tasks=tasks, class_id=id, class_name=class_name)


@app.route('/task-completed', methods=['POST'])
def task_completed():
    '''
    Adds task status to database (TaskComplete table).
    Returns a json response.
    '''
    task_id = request.form.get("task_id")
    student = Student.query.filter_by(email=session['username']).first()
    student_id = student.student_id
    task = Task.query.get(task_id)

    existing = TaskComplete.query.filter_by(
        student_id=student_id, task_id=task_id).first()

    if existing is None:
        '''
        When a student has completed a task, add task status
        to TaskComplete table.
        '''
        if task.required_approval:
            task_complete = TaskComplete(
                task_status="pending", student_id=student_id, task_id=task_id)
            db.session.add(task_complete)

            status = "add"
            task_status = task_complete.task_status
        else:
            '''
            If task does not require approval, automatically set status as
            "accepted".
            '''
            task_complete = TaskComplete(
                task_status="accepted", student_id=student_id, task_id=task_id)
            db.session.add(task_complete)

            status = "add"
            task_status = task_complete.task_status
    else:
        '''
        Deleting means the student has NOT completed the task.
        (A student can say they have completed a task and then undo the action.)
        '''
        db.session.delete(existing)
        status = "delete"
        task_status = "delete"

    db.session.commit()
    return json.dumps({'status': status, 'task_id': task_id, 'student_id': student_id, 'task_status': task_status})


@app.route('/task-delete', methods=['POST'])
def task_delete():
    '''
    Delete task from database.
    Returns a json response.
    '''
    task_id = request.form.get("task_id")
    task_complete = TaskComplete.query.filter_by(task_id=task_id).delete()
    task = Task.query.get(task_id)

    db.session.delete(task)
    db.session.commit()
    return json.dumps({'status': task_id + " deleted"})


@app.route('/learn', defaults={'id': None})
@app.route('/learn/<id>')
def learn(id):
    '''
    Renders learning resources page.
    '''
    if id is None:
        '''
        If id of resource is not specified on url, query all learning resources.
        '''
        resource_list = Resource.query.all()
        return render_template('learn.html', resource_list=resource_list)
    else:
        '''
        If id of resource is specified on url, query only the specified resource.
        '''
        resource = Resource.query.get(id)
        return render_template('learn_details.html', resource=resource)


@app.route("/class")
def class_list():
    '''
    Renders class list page.
    '''
    teacher = Teacher.query.filter_by(email=session['username']).first()
    class_list = teacher.classes.all()
    total_student = {}
    # Count number of students in each class
    for i in class_list:
        class_no = i.class_no.all()
        total = len(class_no)
        total_student[i.class_id] = total
    return render_template('class_list.html', class_list=class_list, total_student=total_student)


@app.route("/manage-class/<id>")
def manage_class(id):
    '''
    Renders manage class page.
    '''
    teacher_classes = TeacherClasses.query.filter_by(class_id=id).first()
    session['award_class_id'] = id
    session['award_class_name'] = teacher_classes.class_name
    class_no = teacher_classes.class_no.all() # List of all students in class

    student_list = {}
    for i in class_no:
        total = 0
        status = []
        student = Student.query.get(i.student_id)
        class_members = student.classes_student.first()
        all_task = student.student_task_done.all()

        # Count the number of pending tasks the student has
        for task in all_task:
            if task.task_status == "pending":
                total += 1

        status.append(class_members.student_status)
        status.append(total)

        user = User.query.filter_by(email=student.email).first()
        new = {user: status}
        student_list.update(new)

    return render_template('manage_class.html', student_list=student_list, teacher_classes=teacher_classes)


@app.route("/manage-student/<id>")
def manage_student(id):
    user = User.query.get(id)
    student = user.student_email.first()
    student_class = student.classes_student.first()
    task_list = Task.query.filter_by(class_id=student_class.class_id).all()
    completed_task = student.student_task_done.all()
    incomplete = []
    completeds = []
    pending = {}
    pending_list = []
    rejected = []
    for task in task_list:
        if len(completed_task) == 0:
            incomplete.append(task)
        else:
            for completed in completed_task:
                if task.task_id == completed.task_id and completed.task_status == "accepted":
                    completeds.append(task)
                    break
                elif task.task_id == completed.task_id and completed.task_status == "pending":
                    pending_list.append(task)
                    new = {task: completed.task_complete_id}
                    pending.update(new)
                    break
                elif task.task_id == completed.task_id and completed.task_status == "rejected":
                    rejected.append(task)
                    break
                else:
                    if task not in incomplete:
                        incomplete.append(task)

    for task in incomplete[:]:
        if task in completeds or task in rejected or task in pending_list:
            incomplete.remove(task)

    return render_template('manage_student.html', incomplete=incomplete,
                           completed=completeds, pending=pending, rejected=rejected, user=user, student=student)


@app.route("/approve-task/<id>")
def approve_task(id):
    task = TaskComplete.query.get(id)
    task.task_status = "accepted"
    db.session.commit()
    return jsonify(status='ok')


@app.route("/reject-task/<id>")
def reject_task(id):
    task = TaskComplete.query.get(id)
    task.task_status = "rejected"
    db.session.commit()
    return jsonify(status='ok')


@app.route("/approve-student/<id>")
def approve_student(id):
    user = User.query.get(id)
    student = user.student_email.first()
    class_members = student.classes_student.first()
    class_members.student_status = "accepted"
    db.session.commit()
    return jsonify(status='ok')


@app.route("/reject-student/<id>")
def reject_student(id):
    user = User.query.get(id)
    student = user.student_email.first()
    class_members = student.classes_student.first()
    class_members.student_status = "rejected"
    db.session.commit()
    return jsonify(status='ok')


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


@app.route('/leaderboard', defaults={'id': None})
@app.route('/leaderboard/<id>')
def leaderboard(id):
    if session['role'] == "student":
        student = Student.query.filter_by(email=session['username']).first()
        class_members = student.classes_student.first()
        teacher_classes = TeacherClasses.query.filter_by(
            class_id=class_members.class_id).first()
    elif id != None:
        # class_members = ClassMembers.query.filter_by(class_id=id).first()
        teacher_classes = TeacherClasses.query.filter_by(class_id=id).first()

    if session['role'] == "student" or id != None:
        # get teacher's name
        teacher = Teacher.query.filter_by(
            teacher_id=teacher_classes.teacher_id).first()
        teacher_user = User.query.filter_by(email=teacher.email).first()
        teacher_name = teacher_user.first_name + " " + teacher_user.last_name
        if teacher_name[-1] == 's':
            teacher_name = teacher_name + "'"
        else:
            teacher_name = teacher_name + "'s"

        # get all members of class
        all_members = ClassMembers.query.filter_by(
            class_id=teacher_classes.class_id, student_status="accepted").all()
        leaderboard = {}

        # calculate points
        for i in all_members:
            points = 0
            all_task_completed = TaskComplete.query.filter_by(
                student_id=i.student_id).all()
            for j in all_task_completed:
                if j.task_status == "accepted":
                    task = Task.query.filter_by(task_id=j.task_id).first()
                    points += task.points

            current_student = Student.query.filter_by(
                student_id=i.student_id).first()
            current_user = User.query.filter_by(
                email=current_student.email).first()
            name = current_user.first_name + " " + current_user.last_name
            new = {i.student_id: (name, points)}
            # key being student_id instead of name is intentional
            leaderboard.update(new)

        sorted_leaderboard = sorted(
            leaderboard.items(), key=lambda x: x[1][1], reverse=True)
        return render_template('student_leaderboard.html', leaderboard=sorted_leaderboard,
                               teacher=teacher_name, class_name=teacher_classes.class_name)
    else:
        teacher = Teacher.query.filter_by(email=session['username']).first()
        class_list = teacher.classes.all()
        leaderboard = {}

        # calculate points
        for i in class_list:
            points = 0
            all_members = ClassMembers.query.filter_by(
                class_id=i.class_id, student_status="accepted").all()
            for j in all_members:
                all_task_completed = TaskComplete.query.filter_by(
                    student_id=j.student_id).all()
                for k in all_task_completed:
                    if k.task_status == "accepted":
                        task = Task.query.filter_by(task_id=k.task_id).first()
                        points += task.points
            new = {i.class_id: (i.class_name, points)}
            # key being class_id instead of name is intentional
            leaderboard.update(new)

        sorted_leaderboard = sorted(
            leaderboard.items(), key=lambda x: x[1][1], reverse=True)
        return render_template('teacher_leaderboard.html', leaderboard=sorted_leaderboard)


@app.route("/profile", methods=['POST', 'GET'])
def profile():
    form = StudentClassForm()
    if form.validate_on_submit():
        class_code = form.data['class_code']
        teacher_classes = TeacherClasses.query.filter_by(
            class_code=class_code).first()
        student = Student.query.filter_by(email=session['username']).first()
        class_member = ClassMembers(
            class_=teacher_classes, student=student, student_status="pending")
        session['status'] = "pending"
        db.session.add(class_member)
        db.session.commit()

    if (session['role'] == "teacher"):
        teacher = Teacher.query.filter_by(email=session['username']).first()
        class_list = teacher.classes.all()
        return render_template('profile.html', email=session['username'], first_name=session['first_name'], last_name=session['last_name'],
                               role="Teacher", school=session['school'], classes=class_list)
    else:
        student = Student.query.filter_by(email=session['username']).first()
        user = User.query.filter_by(email=session['username']).first()
        class_members = student.classes_student.first()

        if class_members and class_members.student_status == "accepted":
            all_members = ClassMembers.query.filter_by(
                class_id=class_members.class_id, student_status="accepted").all()
            leaderboard = {}

            # get class name
            class_name = TeacherClasses.query.filter_by(
                class_id=class_members.class_id).first().class_name

            for i in all_members:
                points = 0
                all_task_completed = TaskComplete.query.filter_by(
                    student_id=i.student_id).all()
                for j in all_task_completed:
                    if j.task_status == "accepted":
                        task = Task.query.filter_by(task_id=j.task_id).first()
                        points += task.points
                new = {i.student_id: points}
                leaderboard.update(new)

            sorted_leaderboard = sorted(
                leaderboard.items(), key=lambda x: x[1], reverse=True)

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
                                   ranking=rank, total=len(leaderboard), points=point, class_name=class_name,
                                   student_status=class_members.student_status, user=user)
        else:
            if class_members:
                status = class_members.student_status
            else:
                status = "empty"
            return render_template('profile.html', email=session['username'],
                                   first_name=session['first_name'], last_name=session['last_name'],
                                   role="Student", school=session['school'], student_status=status, form=form)


@app.route("/student-profile/<id>")
def student_profile(id):
    user = User.query.get(id)
    student = user.student_email.first()
    class_members = student.classes_student.first()
    teacher_classes = TeacherClasses.query.filter_by(
        class_id=class_members.class_id).first()
    if class_members and class_members.student_status == "accepted":
        all_members = ClassMembers.query.filter_by(
            class_id=class_members.class_id, student_status="accepted").all()
        leaderboard = {}

        # get class name
        class_name = TeacherClasses.query.filter_by(
            class_id=class_members.class_id).first().class_name

        for i in all_members:
            points = 0
            all_task_completed = TaskComplete.query.filter_by(
                student_id=i.student_id).all()
            for j in all_task_completed:
                if j.task_status == "accepted":
                    task = Task.query.filter_by(task_id=j.task_id).first()
                    points += task.points
            new = {i.student_id: points}
            leaderboard.update(new)

        sorted_leaderboard = sorted(
            leaderboard.items(), key=lambda x: x[1], reverse=True)

        rank = 1
        point = 0
        for j in sorted_leaderboard:
            id = int(j[0])
            if not (id == student.student_id):
                rank += 1
            else:
                point = j[1]
                break

        return render_template('profile.html', email=user.email,
                               first_name=user.first_name, last_name=user.last_name,
                               role="Student", school=user.school, leaderboard=sorted_leaderboard,
                               ranking=rank, total=len(leaderboard), points=point, class_name=class_name,
                               student_status=class_members.student_status, user=user, teacher_classes=teacher_classes)
    else:
        if class_members:
            status = class_members.student_status
        else:
            status = "empty"
        return render_template('profile.html', email=session['username'],
                               first_name=session['first_name'], last_name=session['last_name'],
                               role="Student", school=session['school'], student_status=status)


def get_all_badges(id):
    badge_owned = Badge.query.filter_by(student_id=id).all()
    return badge_owned


@app.route('/award0', methods=['GET', 'POST'])
def give_class_award():
    teacher = Teacher.query.filter_by(email=session['username']).first()
    available_classes = teacher.classes.all()
    class_list = [(i.class_id, i.class_name) for i in available_classes]

    form = ChooseClassForm()
    form.class_id.choices = class_list

    if form.validate_on_submit():
        session['award_class_id'] = form.class_id.data
        session['award_class_name'] = get_class_name(form.class_id.data)
        return redirect(url_for('.give_award'))

    return render_template('award0.html', form=form)


@app.route('/award', methods=['GET', 'POST'])
def give_award():
    form = AwardForm()
    available_students = ClassMembers.query.filter_by(
        class_id=session['award_class_id']).all()
    student_list = []

    for x in available_students:
        student_id_x = x.student_id
        student_x = Student.query.filter_by(student_id=student_id_x)
        email_x = student_x.first().email
        user = User.query.filter_by(email=email_x).first()
        name = user.first_name + " " + user.last_name
        student_list.append((student_id_x, name))

    student_list.append((-1, 'All'))
    form.student_names.choices = student_list

    # 2 conditions:
    # first : for individual students. Student field must be filled out
    # second: for entire class. Pick all
    if form.validate_on_submit():
        data = request.form['student_names']

        badge = request.form['images']
        badge_location = '/static/images/badge_images/' + badge
        badge_name = request.form['reward']
        badge_comment = request.form['comment']

        if data == '-1':

            class_chosen = ClassMembers.query.filter_by(
                class_id=session['award_class_id']).all()
            student_ids = []
            for x in class_chosen:
                student_ids.append(x.student_id)

            for i in student_ids:
                student = Student.query.filter_by(student_id=i).first()
                badge_1 = Badge(badge_name=badge_name, badge_comment=badge_comment,
                                badge_location=badge_location, student_id=student.student_id)
                db.session.add(badge_1)

            db.session.commit()
            return redirect(url_for('.give_class_award'))

        else:
            student = Student.query.filter_by(
                student_id=request.form['student_names']).first()
            badge_x = Badge(badge_name=badge_name, badge_comment=badge_comment,
                            badge_location=badge_location, student_id=student.student_id)
            db.session.add(badge_x)
            db.session.commit()
            user = User.query.filter_by(email=student.email).first()
            return redirect(url_for('view_awards', id=user.id))

    return render_template('award.html', form=form, class_name=session['award_class_name'])


@app.route('/award-direct/<id>', methods=['GET', 'POST'])
def give_award_directly(id):
    form = AwardForm()
    available_students = ClassMembers.query.filter_by(student_id=id).all()
    student_list = []

    for x in available_students:

        student_id_x = x.student_id
        student_x = Student.query.filter_by(student_id=student_id_x)
        email_x = student_x.first().email
        user = User.query.filter_by(email=email_x).first()
        name = user.first_name + " " + user.last_name
        student_list.append((student_id_x, name))

    form.student_names.choices = student_list

    if form.validate_on_submit():
        data = request.form['student_names']

        badge = request.form['images']
        badge_location = '/static/images/badge_images/' + badge
        badge_name = request.form['reward']
        badge_comment = request.form['comment']

        student = Student.query.filter_by(
            student_id=request.form['student_names']).first()
        badge_x = Badge(badge_name=badge_name, badge_comment=badge_comment,
                        badge_location=badge_location, student_id=student.student_id)
        db.session.add(badge_x)
        db.session.commit()
        user = User.query.filter_by(email=student.email).first()
        return redirect(url_for('view_awards', id=user.id))
    return render_template('award.html', form=form, student_id=id, class_name=session['award_class_name'])


@app.route("/view-awards/<id>")
def view_awards(id):
    # pass on student and his badges
    user = User.query.get(id)
    student = user.student_email.first()

    badge_list = get_all_badges(student.student_id)
    return render_template('view_awards.html', user=user, student=student, badge_list=badge_list)


def get_class_name(id):
    teacher_class = TeacherClasses.query.filter_by(class_id=id).first()
    return teacher_class.class_name
