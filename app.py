from ast import If
import os
from flask import Flask, session, request, redirect, render_template, g, flash, url_for, jsonify
import json
import database.db_queries
import uuid
import re
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

# LINK THAT SHOWS HOW TO USE AJAX w/ flask: https://www.youtube.com/watch?v=UmC26YXExJ4
# or this one: https://joseph-dougal.medium.com/flask-ajax-bootstrap-tables-9036410cbc8
# HOW TO MAKE OUR APP A SPA if we have time... https://blog.miguelgrinberg.com/post/how-to-deploy-a-react-router-flask-application
# another one: https://dev.to/nagatodev/how-to-connect-flask-to-reactjs-1k8i

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
                if user['status'] == "inactive" and user['role'] != 'admin':
                    flash('Account not activated. Contact an admin.')
                    return(redirect(url_for('login')))

                session['username'] = username;
                session['role'] = database.db_queries.get_user_role(username)[0][0]
                database.db_queries.update_status_by_username(username, 'active')
                # print(json.loads(database.db_queries.get_user_by_username(session['username'])[0][0])[0])
                if session['role'] == 'instructor':
                    session['course_list'] = json.loads(
                        database.db_queries.get_teachers_courses(session['username'])[0][0])
                else:
                    session['course_list'] = json.loads(database.db_queries.get_students_courses(session['username'])[0][0])
                    # print(json.loads(database.db_queries.get_teachers_courses(session['username'])[0][0]))

                return(redirect(url_for('dashboard')))

        flash('Incorrect username or password')
        return(redirect(url_for('login')))
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
        user_id = request.form['user_id']
        password = request.form['pass']
        passwordconfirm = request.form['passconfirm']
        sq1_q = request.form['sq1_q']
        sq1_a = request.form['sq1_a']
        sq2_q = request.form['sq2_q']
        sq2_a = request.form['sq2_a']
        sq3_q = request.form['sq3_q']
        sq3_a = request.form['sq3_a']
        account_type = request.form['account_type']
        
        emailreg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.search(emailreg, username):
            flash('Username must be an email address!')
            return(redirect(url_for('signup')))
        
        idreg = re.compile(r'(^[0-9]+$)')
        if not re.search(idreg, user_id):
            flash('User ID must be number')
            return(redirect(url_for('signup')))

        regx = "^(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,}$"
        passlogic = re.compile(regx)

        if not re.search(passlogic, password):
            flash('Passwords must be 5 chars in length, at least 1 number and 1 symbol')
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
        database.db_queries.add_user(username, account_type, password, fullname, 'inactive', user_id, sq1_q, sq1_a, sq2_q, sq2_a, sq3_q, sq3_a)
        session['username'] = username
        session['role'] = database.db_queries.get_user_role(username)[0][0]
        session['course_list'] = json.loads(database.db_queries.get_students_courses(session['username'])[0][0])
        flash('Account created!')
        return(redirect(url_for('login')))

    return render_template("signup.html")

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        username = request.form['user']
        # check if username already exists
        user_grab = json.loads(database.db_queries.get_users()[0][0])
        for user in user_grab:
            if user['username'] == username:
                session['username'] = username;
                return(redirect(url_for('reset2')))
        
        flash('Username not found!')
        return(redirect(url_for('reset')))

    return render_template("reset.html")

@app.route('/reset2', methods=['GET', 'POST'])
def reset2():
    if request.method == 'POST':
        sq1_a = request.form['sq1_a']
        sq2_a = request.form['sq2_a']
        sq3_a = request.form['sq3_a']
        # check if username already exists
        user = json.loads(database.db_queries.get_user_by_username(session['username'])[0][0])[0]
        if sq1_a == user['sq1_answer'] and sq2_a == user['sq2_answer'] and sq3_a == user['sq3_answer']:
            return(redirect(url_for('reset3')))

        flash('Incorrect answers to security questions!')
        return(redirect(url_for('reset2')))

    user = json.loads(database.db_queries.get_user_by_username(session['username'])[0][0])[0]
    sq1_q = user['sq1']
    sq2_q = user['sq2']
    sq3_q = user['sq3']
    return render_template("reset2.html", sq1_q=sq1_q, sq2_q=sq2_q, sq3_q=sq3_q)

@app.route('/reset3', methods=['GET', 'POST'])
def reset3():
    if request.method == 'POST':
        password = request.form['pass']
        passwordconfirm = request.form['passconfirm']

        regx = "^(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,}$"
        passlogic = re.compile(regx)

        if not re.search(passlogic, password):
            flash('Passwords must be 5 chars in length, at least 1 number and 1 symbol)')
            return(redirect(url_for('reset3')))
        if(password != passwordconfirm):
            flash('Passwords do not match!')
            return(redirect(url_for('reset3')))
    
        database.db_queries.update_password_by_username(password, session['username'])
        [session.pop(key) for key in list(session.keys())]
        flash('Password updated!')
        return(redirect(url_for('login')))
    
    return render_template("reset3.html")

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

    # get num students
    num_students = database.db_queries.get_num_students()[0][0]

    # get num courses
    num_courses = database.db_queries.get_num_courses()[0][0]

    # get num teachers
    num_teachers = database.db_queries.get_num_instructors()[0][0]

    to_do = []
    upcoming = []
    past = []

    if session['role'] == 'instructor':
        al = json.loads(database.db_queries.get_assignment_by_name_teacher(session['username'])[0][0])
        old_al = sorted(al, key=lambda d: datetime.strptime(d['due_date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
        assignment_list = [d for d in old_al if datetime.strptime(d['due_date'], '%Y-%m-%d %H:%M:%S') > datetime.now()]

    
    if session['role'] == 'student':
        al = json.loads(database.db_queries.get_assignment_by_name_student(session['username'])[0][0])
        no_dup = []
        for i in range(len(al)):
            if al[i] not in al[i + 1:]:
                no_dup.append(al[i])
        assignment_list = sorted(no_dup, key=lambda d: datetime.strptime(d['due_date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
        to_do = [d for d in assignment_list if datetime.strptime(d['due_date'], '%Y-%m-%d %H:%M:%S') < datetime.now() + timedelta(days=3) and datetime.strptime(d['due_date'], '%Y-%m-%d %H:%M:%S') > datetime.now()]
        upcoming = [d for d in assignment_list if datetime.strptime(d['due_date'], '%Y-%m-%d %H:%M:%S') > datetime.now() + timedelta(days=3)]
        past = [d for d in assignment_list if datetime.strptime(d['due_date'], '%Y-%m-%d %H:%M:%S') < datetime.now()]

    if session['role'] == 'admin':
        return render_template("dashboard.html", course_list=session['course_list'], role=session['role'],
                               num_students=num_students, num_courses=num_courses, num_teachers=num_teachers,
                               assignment_list='', to_do='', upcoming='', past='')

    return render_template("dashboard.html", course_list=session['course_list'], role=session['role'], num_students=num_students, num_courses=num_courses, num_teachers=num_teachers, assignment_list = assignment_list, to_do=to_do, upcoming=upcoming, past=past)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        if 'name' in request.form:
            new_name = request.form['name']
            database.db_queries.update_name_by_username(session['username'], new_name)
        if 'email' in request.form:
            print("EMAIL CHANGE")
            new_email = request.form['email']
            emailreg = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if not re.search(emailreg, new_email):
                flash('Username must be an email address!')
                return(redirect(url_for('profile')))
            database.db_queries.update_email_by_username(session['username'], new_email)
            flash('Username updated')
            return(redirect(url_for('profile')))
        if 'id' in request.form:
            print("ID CHANGE")
            new_id = request.form['id']
            idreg = re.compile(r'(^[0-9]+$)')
            if not re.search(idreg, new_id):
                flash('User ID must be number')
                return(redirect(url_for('profile')))
            database.db_queries.update_id_by_username(session['username'], new_id)
            flash('User ID updated')
            return(redirect(url_for('profile')))
        
        if 'current' in request.form:
            user = json.loads(database.db_queries.get_user_by_username(session['username'])[0][0])[0]
            print(user)
            if request.form['current'] == user['password']:
                new_pass = request.form['new']
                regx = "^(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{5,}$"
                passlogic = re.compile(regx)

                if not re.search(passlogic, new_pass):
                    flash('Passwords must be 5 chars in length, at least 1 number and 1 symbol)')
                    return(redirect(url_for('profile')))

                confirm_pass = request.form['confirm']
                if(new_pass != confirm_pass):
                    flash('Passwords do not match!')
                    return(redirect(url_for('profile')))

                database.db_queries.update_password_by_username(session['username'], new_pass)
                print(" SHOULD BE UPDATED")
                # print(database.db_queries.get_user_by_username(session['username']))
                flash('Password updated!')
                return(redirect(url_for('profile')))
            
            flash('Incorrect current password!')
            return(redirect(url_for('profile')))
        
        if 'sq1_q' in request.form:
            if 'sq1_a' not in request.form:
                flash('Must provide answer to new question!')
                return(redirect(url_for('profile')))
            sq1_q = request.form['sq1_q']
        if 'sq2_q' in request.form:
            if 'sq2_a' not in request.form:
                flash('Must provide answer to new question!')
                return(redirect(url_for('profile')))
            sq2_q = request.form['sq2_q']
        if 'sq3_q' in request.form:
            if 'sq3_a' not in request.form:
                flash('Must provide answer to new question!')
                return(redirect(url_for('profile')))
            sq3_q = request.form['sq3_q']



        return redirect(url_for('profile'))

    # get all user data with username
    user_data = json.loads(database.db_queries.get_user_by_username(session['username'])[0][0])
    print(user_data)
    user_data = user_data[0]
    return render_template("profile.html", course_list=session['course_list'], role=session['role'], user=user_data)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        print("IN POST")
        if 'name' in request.form:
            print("NAME in request form")
            new_name = request.form['name']
            database.db_queries.update_name_by_username(session['username'], new_name)
        if 'status' in request.form:
            print("STATUS in request form")
            username = request.form['username']
            status = request.form['status']
            if status == 'active':
                database.db_queries.update_status_by_username(username, 'inactive')
            else:
                database.db_queries.update_status_by_username(username, 'active')

        # assign teacher to course
        if 'teacher_username' in request.form:
            print("teacher username in form")
            teacher_username = request.form['teacher_username']
            course_ids = request.form.getlist('course_id')
            print("PRINTING OCURSE IDS:" + str(course_ids))
            print("PRINTING teacher username:" + str(teacher_username))
            for id in course_ids:
                database.db_queries.update_instructor_by_course_id(id, teacher_username)

        # assign student to course
        if 'student_username' in request.form:
            print("student username in form")
            student_username = request.form['student_username']
            course_ids = request.form.getlist('course_id')
            print("PRINTING OCURSE IDS:" + str(course_ids))
            print("PRINTING student username:" + str(student_username))
            for id in course_ids:
                if id != '' and student_username != '':
                    database.db_queries.enroll_in_course(student_username, id)

        users = json.loads(database.db_queries.get_users()[0][0])
        return redirect(url_for("settings"))

    users = json.loads(database.db_queries.get_users()[0][0])
    courses_instructor = json.loads(database.db_queries.get_courses_no_instructor()[0][0])
    print("PRINTING instructor courses:" + str(courses_instructor))
    all_students = json.loads(database.db_queries.get_all_student_usernames()[0][0])
    courses_student = {}
    for student in all_students:
        courses_student[student['username']] = json.loads(database.db_queries.get_courses_not_enrolled(student['username'])[0][0])
    return render_template("settings.html", course_list=session['course_list'], users=users, role=session['role'], courses_instructor=courses_instructor, courses_student=courses_student)

@app.route('/course_admin')
def course_admin():
    return render_template("course_admin.html", role=session['role'])

@app.route('/create_course', methods=['POST', 'GET'])
def create_course():
    if request.method == 'POST':
        course_name = request.form['course_name']
        instructor_username = request.form.get('instructor_username')
        if instructor_username == None:
            instructor_username = ''
        capacity = request.form.get('capacity')
        description = request.form['description']
        database.db_queries.add_course(course_name, instructor_username, description, capacity)

    instructors = json.loads(database.db_queries.get_all_active_instructors()[0][0])
    return render_template("create_course.html", role=session['role'], instructors=instructors)

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

    return render_template("courses/home.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], recent_announcements=recent_announcements, instructor=instructor[0], role=session['role'])

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

    return render_template("courses/announcements_view.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], announcement=single_announcement, instructor=instructor[0], role=session['role'])

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

    return render_template("courses/announcements_create.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], role=session['role'])

@app.route('/<course_id>/assignments_view/<assignment_id>/<view_type>', methods=['GET', 'POST'])
def view_assignment(course_id, assignment_id, view_type):
    print("in the func")
    if request.method == 'POST':
        print("in the func2")
        submission = request.form['submission']
        student = request.form['student']
        assignment_id = request.form['id']
        print('Submission: ' + submission)
        print('student:  ' +  student)
        print('assignment_id: ' + assignment_id)
        database.db_queries.submit_assignment(assignment_id, student, submission)
    assignments = json.loads(
                    database.db_queries.get_students_grades_for_course(session['username'], course_id)[0][0])
    single_assignment = {}
    for assignment in assignments:
        if assignment['assignment_id'] == int(assignment_id):
            single_assignment = assignment
            print(single_assignment)
            break
    
    # get instructor for announcements
    instructor = json.loads(
                    database.db_queries.get_instructor_course_id(course_id)[0][0])

    course_name = get_course_name(course_id)
    return render_template("courses/assignments_view.html", course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'], assignment=single_assignment, instructor=instructor[0], role=session['role'], view_type=view_type)

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
                    database.db_queries.get_teachers_assignments_for_course(session['username'], course_id)[0][0])
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
    return render_template("courses/assignments_create.html", role=session['role'], course_list=session['course_list'], course_id=course_id, course_name=course_name['course_name'])

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

# TODO: edit account
# @app.route("/edit_account.html", methods=['GET', 'POST'])
# def update_username():
#     username = json.loads(database.db_queries.get_user_by_username(session['username']))
# def update_security_question():
#     pass
