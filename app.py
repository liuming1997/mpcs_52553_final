import os
from flask import Flask, session, request, redirect, render_template, g, flash, url_for
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
        user_grab = database.db_queries.get_users()

        # check that username and password are correct
        for user in user_grab:
            if user[0] == username and user[2] == password:
                session['username'] = username;
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
        session['username'] = username
        return(redirect(url_for('dashboard')))

    return render_template("signup.html")

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/settings')
def settings():
    return render_template("settings.html") 


# course routes
@app.route('/courses/home')
def courses():
    return render_template("courses/home.html")

@app.route('/courses/announcements')
def course_announcements():
    return render_template("courses/announcements.html")

@app.route('/courses/announcements_view')
def view_announcement():
    return render_template("courses/announcements_view.html")

@app.route('/courses/announcements_create')
def create_announcement():
    return render_template("courses/announcements_create.html")

@app.route('/courses/assignments')
def course_assignments():
    return render_template("courses/assignments.html")

@app.route('/courses/assignments_view')
def view_assignment():
    return render_template("courses/assignments_view.html")

@app.route('/courses/grades')
def course_grades():
    return render_template("courses/grades.html")

@app.route('/courses/home')
def course_home():
    return render_template("courses/home.html")

@app.route('/courses/modules')
def course_modules():
    return render_template("courses/modules.html")

@app.route('/courses/syllabus')
def course_syllabus():
    return render_template("courses/syllabus.html")

# @app.route('/courses/<course>')
# def course_syllabus():
#     return render_template("courses/course.html")
