from ast import If
import os
from flask import Flask, session, request, redirect, render_template, g, flash, url_for, jsonify
import json
import database.db_queries
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

# LINK THAT SHOWS HOW TO USE AJAX w/ flask: https://www.youtube.com/watch?v=UmC26YXExJ4


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
            if user['username'] == username and user['password'] == password:
                session['username'] = username;
                session['role'] = database.db_queries.get_user_role(username)[0][0]
                if session['role'] == 'instructor':
                    session['course_list'] = json.loads(
                        database.db_queries.get_teachers_courses(session['username'])[0][0])
                else:
                    session['course_list'] = json.loads(database.db_queries.get_students_courses(session['username'])[0][0])
                print(json.loads(database.db_queries.get_teachers_courses(session['username'])[0][0]))

                return(redirect(url_for('dashboard')))
            else:
                flash('Incorrect username or password')
    return render_template("login.html")

@app.route('/logout')
def logout():
    [session.pop(key) for key in list(session.keys())]
    return render_template("logout.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['name']
        username = request.form['user']
        password = request.form['pass']
        passwordconfirm = request.form['passconfirm']
        sq1_q = request.form['sq1_q']
        sq1_a = request.form['sq1_a']
        sq2_q = request.form['sq2_q']
        sq2_a = request.form['sq2_a']
        sq3_q = request.form['sq3_q']
        sq3_a = request.form['sq3_a']
        account_type = request.form['account_type']

        regx = "^(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,}$"
        passlogic = regx.compile(regx)

        if not regx.search(passlogic, password):
            flash('Passwords must be 5 chars in length, at least 1 number and 1 symbol)')
            return(redirect(url_for('signup')))
        if(password != passwordconfirm):
            flash('Passwords do not match!')
            return(redirect(url_for('signup')))

        # check if username already exists
        user_grab = database.db_queries.get_users()
        for user in user_grab:
            if user[0] == username:
                flash('Username already exists!')
                return(redirect(url_for('signup')))

        # add user
        database.db_queries.add_user(username, account_type, password, fullname, sq1_q, sq1_a, sq2_q, sq2_a, sq3_q, sq3_a)
        session['username'] = username
        session['role'] = database.db_queries.get_user_role(username)[0][0]
        session['course_list'] = json.loads(database.db_queries.get_students_courses(session['username'])[0][0])
        return(redirect(url_for('dashboard')))

    return render_template("signup.html")

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        username = request.form('user')
        # check if username already exists
        user_grab = database.db_queries.get_users()
        for user in user_grab:
            if user[0] == username:
                session['username'] = username;
                return(redirect(url_for('reset2')))
        
        flash('Username not found!')
        return(redirect(url_for('reset')))

    return render_template("reset.html")

@app.route('/reset2', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        sq1_a = request.form('sq1_a')
        sq2_a = request.form('sq2_a')
        sq3_a = request.form('sq3_a')
        # check if username already exists
        user_grab = database.db_queries.get_users()
        for user in user_grab:
            if user[0] == username:
                session['username'] = username;
                return(redirect(url_for('reset3')))
        
        flash('Username not found!')
        return(redirect(url_for('reset')))

    return render_template("reset2.html")

@app.route('/')
def index():
    if not session.get('username'):
        # Visitor is unknown, return to login
        return redirect(url_for('login'))
    return redirect(url_for("dashboard"))

@app.route('/edit_account', methods=['GET', 'POST'])
def edit_account():
    if request.method == 'POST':
        new_name = request.form['name']
        new_username = request.form['username']

        # update user information here

        return(redirect(url_for('dashboard')))
    return render_template("edit.html")

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
@app.route('/<course_id>/home')
def course_home(course_id):
    course_announcements = json.loads(
                        database.db_queries.get_announcements_course_id(course_id)[0][0])
    # print(course_announcements)
    recent_announcements = sorted(course_announcements, key=lambda d: datetime.strptime(d['date_posted'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    # sorted(data.items(), key = lambda x:datetime.strptime(x[0], '%d-%m-%Y'), reverse=True)

    del recent_announcements[4:]

    # get instructor for announcements
    instructor = json.loads(
                        database.db_queries.get_instructor_course_id(course_id)[0][0])

    course_name = get_course_name(course_id)

    return render_template("courses/home.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], recent_announcements=recent_announcements, instructor=instructor[0])

@app.route('/<course_id>/announcements')
def course_announcements(course_id):
    course_announcements = json.loads(
                    database.db_queries.get_announcements_course_id(course_id)[0][0])

    # get instructor for announcements
    instructor = json.loads(
                    database.db_queries.get_instructor_course_id(course_id)[0][0])

    course_name = get_course_name(course_id)

    sorted_announcements = sorted(course_announcements, key=lambda d: datetime.strptime(d['date_posted'], '%Y-%m-%d %H:%M:%S'), reverse=True)

    return render_template("courses/announcements.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], course_announcements=sorted_announcements, instructor=instructor[0], role=session['role'])

@app.route('/<course_id>/announcements_view/<announcement_id>')
def view_announcement(course_id, announcement_id):
    course_announcements = json.loads(
                    database.db_queries.get_announcements_course_id(course_id)[0][0])
    single_announcement = {}
    for announcement in course_announcements:
        if announcement['announcement_id'] == int(announcement_id):
            single_announcement = announcement
            break
    
    # get instructor for announcements
    instructor = json.loads(
                    database.db_queries.get_instructor_course_id(course_id)[0][0])
    
    course_name = get_course_name(course_id)

    return render_template("courses/announcements_view.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], announcement=single_announcement, instructor=instructor[0])

@app.route('/<course_id>/announcements_create', methods=['GET', 'POST'])
def create_announcement(course_id):
    course_name = get_course_name(course_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        print(title)
        print(content)
        database.db_queries.add_announcement(course_id, title, content)
        return redirect(url_for('course_home', course_id=course_id))

    return render_template("courses/announcements_create.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'])

@app.route('/<course_id>/assignments_view/<assignment_id>')
def view_assignment(course_id, assignment_id):
    assignments = json.loads(
                    database.db_queries.get_students_grades_for_course(session['username'], course_id)[0][0])
    single_assignment = {}
    for assignment in assignments:
        if assignment['assignment_id'] == int(assignment_id):
            single_assignment = assignment
            break
    
    # get instructor for announcements
    instructor = json.loads(
                    database.db_queries.get_instructor_course_id(course_id)[0][0])

    course_name = get_course_name(course_id)
    return render_template("courses/assignments_view.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], assignment=single_assignment, instructor=instructor[0])

@app.route('/<course_id>/assignments')
def course_assignments(course_id):
    assignments = []
    print(session['role'])
    if session['role'] ==  'student':
        assignments = json.loads(
                    database.db_queries.get_students_grades_for_course(session['username'], course_id)[0][0])
        #updated_assignments = [x for x in assignments if x['date_submitted'] == None]
        updated_assignments = assignments
    elif session['role'] ==  'instructor':
        assignments = json.loads(
                    # this query loads the appropriate data w/ new assignments
                    database.db_queries.get_assignments_course_id(course_id)[0][0])
        # updated_assignments = [x for x in assignments if x['date_submitted'] == None]
        updated_assignments = assignments

        print(assignments)
        print(updated_assignments)
    course_name = get_course_name(course_id)
    return render_template("courses/assignments.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], assignments=updated_assignments, role=session['role'])

@app.route('/<course_id>/assignments_create', methods=['POST', 'GET'])
def create_assignment(course_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        points = request.form['points']
        due_date = request.form['due_date']
        database.db_queries.add_assignment(course_id, title, content, points, due_date)

    course_name = get_course_name(course_id)
    return render_template("courses/assignments_create.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'])

@app.route('/<course_id>/grades', methods=['GET', 'POST'])
def course_grades(course_id):
    if request.method == 'POST':
        grade = request.form['grade']
        student = request.form['student']
        id = request.form['id']
        database.db_queries.grade_assignment(student, id, grade)
        return redirect(url_for('course_grades', course_id=course_id))

    if session['role'] ==  'student':
        assignments = json.loads(
                    database.db_queries.get_students_grades_for_course(session['username'], course_id)[0][0])
        updated_assignments = [x for x in assignments if x['date_submitted'] != None]
        # updated_assignments = assignments
    elif session['role'] ==  'instructor':
        assignments = json.loads(
                    database.db_queries.get_all_students_grades_for_course(course_id)[0][0])
        updated_assignments = [x for x in assignments if x['date_submitted'] != None]
        # updated_assignments = assignments
    course_name = get_course_name(course_id)
    return render_template("courses/grades.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], role=session['role'], assignments=updated_assignments)

def get_course_name(course_id):
    course_name = json.loads(
                    database.db_queries.get_coursename_course_id(course_id)[0][0])
    return course_name[0]

