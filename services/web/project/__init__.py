import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for,
    render_template,
    session
)
from flask_sqlalchemy import SQLAlchemy
from .models import db, User
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
        user = User(role=session['role'], email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, password=form.password.data, school=form.school.data)
        db.session.add(user)
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
