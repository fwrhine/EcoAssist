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


app = Flask(__name__)
app.config.from_object("project.config.Config")
db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
    trial = db.session.execute("select * from trial;")
    return render_template("index.html",trial = trial)

@app.route("/loginpage",  methods=['POST', 'GET'])
def loginPage():
     return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    print(session['logged_in'])
    reqUsername = request.form["username"]
    print(reqUsername)
    reqPassword = request.form["password"]
    print(reqPassword)
        
    user = db.session.execute('select * from use')
    for i in user:
        userDict = dict(i)
        name = userDict['username']
        passw = userDict['password']
        print(name+passw)

        if name == reqUsername and passw == reqPassword:
            print("suc")
            session['logged_in'] = True
            session['username'] = name
            return homePage()
           
    print("fail")
    return loginPage()
        

@app.route('/registerpage',methods=['POST', 'GET'])
def registerPage():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    reqUsername = request.form["username"]
    print(reqUsername)
    reqPassword = request.form["password"]
    print(reqPassword)

    db.session.execute("insert into use(username, password) values('"+reqUsername+"', '"+reqPassword+"');")
    db.session.commit()
    # user = Use()
    # db.session.add(user)
    session['username'] = reqUsername
    return homePage()


@app.route('/homepage',methods=['POST', 'GET'])
def homePage():
    name = session['username']
    return render_template('main.html', name = name)

@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    session['logged_in'] = False
    return index()
