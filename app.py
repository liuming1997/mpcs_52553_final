import os
from flask import Flask, session, request, redirect, render_template, g, flash, url_for, jsonify
import json
import database.db_queries
import uuid

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex


# @app.before_request
# def before_request_check():
#     if not session.get('id'):
#         # Visitor is unknown, return to login
#         return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        user_grab = database.db_queries.get_users()[0][0]
        user_list = json.loads(user_grab)

        # check that username and password are correct
        for user in user_list:
            print(user)
            print(username + " : " + user['username'])
            if user['username'] == username and user['password'] == password:
                session['username'] = username;
                session['course_list'] = json.loads(database.db_queries.get_students_courses(session['username'])[0][0])
                return(redirect(url_for('dashboard')))
            else:
                flash('Incorrect username or password')
    return render_template("login.html")

@app.route('/logout')
def logout():
    [session.pop(key) for key in list(session.keys())]
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['name']
        username = request.form['user']
        password = request.form['pass']
        account_type = request.form['account_type']

        # check if username already exists
        user_grab = database.db_queries.get_users()
        for user in user_grab:
            if user[0] == username:
                flash('Username already exists!')
                return(redirect(url_for('signup')))

        # add user
        database.db_queries.insert_new_user(fullname, username, password, account_type)
        print(database.db_queries.get_users())
        session['username'] = username
        return(redirect(url_for('dashboard')))

    return render_template("signup.html")

@app.route('/reset')
def reset():
    return render_template("reset.html")

@app.route('/')
def index():
    if not session.get('username'):
        # Visitor is unknown, return to login
        return redirect(url_for('login'))
    return redirect(url_for("dashboard"))

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", course_list=session['course_list'])

@app.route('/profile')
def profile():
    return render_template("profile.html", course_list=session['course_list'])

@app.route('/settings')
def settings():
    return render_template("settings.html", course_list=session['course_list']) 


# course routes
@app.route('/<course>/home')
def course_home(course):
    return render_template("courses/home.html", course_list=session['course_list'], course=course)

@app.route('/<course>/announcements')
def course_announcements(course):
    return render_template("courses/announcements.html", course_list=session['course_list'], course=course)

@app.route('/<course>/announcements_view')
def view_assignment(course):
    return render_template("courses/announcements_view.html", course_list=session['course_list'], course=course)

@app.route('/<course>/assignments_view')
def view_assignment(course):
    return render_template("courses/assignments_view.html", course_list=session['course_list'], course=course)

@app.route('/<course>/assignments')
def course_assignments(course):
    return render_template("courses/assignments.html", course_list=session['course_list'], course=course)

@app.route('/<course>/grades')
def course_grades(course):
    return render_template("courses/grades.html", course_list=session['course_list'], course=course)

@app.route('/<course>/announcements_create')
def create_announcement():
    return render_template("courses/announcements_create.html")

@app.route('/<course>/modules')
def course_modules(course):
    return render_template("courses/modules.html", course_list=session['course_list'], course=course)

@app.route('/<course>/syllabus')
def course_syllabus(course):
    return render_template("courses/syllabus.html", course_list=session['course_list'], course=course)

