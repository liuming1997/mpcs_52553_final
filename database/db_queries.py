import sqlite3
import datetime
# HOW TO FORMAT SQLITE table rows as json: https://database.guide/format-sqlite-results-as-json/

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# add a new user
def insert_new_user(name, username, password, account_type):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, role, password, name) VALUES(?, ?, ?, ?)", (username, account_type, password, name))
    conn.commit()

# get all users
def get_users():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    # test user data
    # cur.execute("SELECT * from users;")
    # return cur.fetchall()
    cur.execute("SELECT json_group_array( json_object( 'username', username, 'role', role, 'password', password, 'name', name, 'status', status ) ) FROM users")
    rows = cur.fetchall()
    print(rows)
    return rows

def get_user_role(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users where username=" + "'" + username + "'")
    rows = cur.fetchall()
    return rows

def get_user_by_username(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    # test user data
    # cur.execute("SELECT * from users;")
    # return cur.fetchall()
    cur.execute(
        "SELECT json_group_array( json_object( 'username', username, 'role', role, 'password', password, 'name', name, 'status', status,  'user_id', user_id, 'sq1', sq1, 'sq2', sq2, 'sq3', sq3, 'sq1_answer', sq1_answer, 'sq2_answer', sq2_answer, 'sq3_answer', sq3_answer) ) FROM users where username=" + "'" + username + "'")
    rows = cur.fetchall()
    print(rows)
    return rows

def get_all_active_instructors():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    # test user data
    # cur.execute("SELECT * from users;")
    # return cur.fetchall()
    cur.execute(
        "SELECT json_group_array( json_object( 'username', username, 'role', role, 'password', password, 'name', name, 'status', status,  'user_id', user_id, 'sq1', sq1, 'sq2', sq2, 'sq3', sq3, 'sq1_answer', sq1_answer, 'sq2_answer', sq2_answer, 'sq3_answer', sq3_answer) ) FROM users where role='instructor' and status='active'")
    rows = cur.fetchall()
    print(rows)
    return rows

# update name of user
def update_name_by_username(username, new_name):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "UPDATE users SET name=? WHERE username=?"
    cur.execute(cmd, (new_name, username))
    conn.commit()

def update_status_by_username(username, new_status):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "UPDATE users SET status=? WHERE username=?"
    cur.execute(cmd, (new_status, username))
    conn.commit()

# update email of user
def update_email_by_username(username, new_email):
    print(new_email)
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "UPDATE users SET username=? WHERE username=?"
    cur.execute(cmd, (username, new_email))
    conn.commit()

# update id of user
def update_id_by_username(username, new_id):
    print(new_id)
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "UPDATE users SET user_id=? WHERE username=?"
    cur.execute(cmd, (username, new_id))
    conn.commit()

# update password of user
def update_password_by_username(username, new_password):
    print(new_password)
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "UPDATE users SET password=? WHERE username=?"
    cur.execute(cmd, (username, new_password))
    conn.commit()

# get num students
def get_num_students():
    conn = create_connection('canvas.db')
    role = 'student'
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) as num_students FROM users where role=" + "'" + role + "'")
    # cur.execute("SELECT json_group_array( json_object( 'num_students', num_students)) FROM (SELECT COUNT(*) as num_students FROM users where role=" + "'" + role +  "'")))

    rows = cur.fetchall()
    return rows

# get num instructors
def get_num_instructors():
    conn = create_connection('canvas.db')
    role = 'instructor'
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM users where role=" + "'" + role + "'")
    # cur.execute("SELECT json_group_array( json_object( 'course_id', course_id, 'course_name', course_name, 'instructor_username', instructor_username)) FROM courses")

    rows = cur.fetchall()
    return rows

# get num courses
def get_num_courses():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM courses")
    # cur.execute("SELECT json_group_array( json_object( 'course_id', course_id, 'course_name', course_name, 'instructor_username', instructor_username)) FROM courses")

    rows = cur.fetchall()
    return rows

# get all courses
def get_courses():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object( 'course_id', course_id, 'course_name', course_name, 'instructor_username', instructor_username)) FROM courses")
    rows = cur.fetchall()
    return rows

# get all announcements
def get_announcements():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object( 'announcement_id', announcement_id, 'course_id', course_id, 'title', title, 'content', content, 'date_posted', date_posted) ) FROM announcements")
    rows = cur.fetchall()
    return rows

# get announcements by course_id
def get_announcements_course_id(course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT json_group_array( json_object( 'announcement_id', announcement_id, 'course_id', course_id, 'title', title, 'content', content, 'date_posted', date_posted) ) FROM announcements where course_id=" + str(course_id))
    rows = cur.fetchall()
    return rows

# get all grades
def get_grades():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT json_group_array( json_object( 'assignment_id', assignment_id, 'student_username', student_username, 'grade', grade) ) FROM grades")
    rows = cur.fetchall()
    return rows

# todo: get all assignments + grades for student
def get_assignments_with_grades_for_student():
    pass

# get assignments
def get_assignments():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT json_group_array( json_object( 'assignment_id', assignment_id, 'course_id', course_id, 'title', title, 'content', content, 'points', points, 'due_date', due_date) ) FROM assignments")
    rows = cur.fetchall()
    return rows

# get assignments by course_id
def get_assignments_course_id(course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT json_group_array( json_object( 'assignment_id', assignment_id, 'course_id', course_id, 'title', title, 'content', content, 'points', points, 'due_date', due_date) ) FROM assignments where course_id=" + str(course_id))
    rows = cur.fetchall()
    return rows

# get assignments by course_id
def get_coursename_course_id(course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT json_group_array( json_object( 'course_name', course_name) ) FROM courses where course_id=" + str(course_id))
    rows = cur.fetchall()
    return rows

# get instructor by course_id
def get_instructor_course_id(course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT json_group_array( json_object( 'instructor_username', instructor_username) ) FROM courses where course_id=" + str(course_id))
    rows = cur.fetchall()
    return rows

# get all takes_course
def get_takes_course():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object( 'username', username, 'course_id', course_id ) ) FROM takes_course")
    rows = cur.fetchall()
    return rows

# get all of a teacher's courses
def get_teachers_courses(username):
    conn = create_connection('canvas.db')
    name = 'Web Dev'
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object( 'course_id', course_id, 'course_name', course_name, 'instructor_username', instructor_username)) FROM courses where instructor_username=" + "'" + username + "'")
    rows = cur.fetchall()
    return rows

# todo: get all of a teacher's assignments
def get_teachers_assignments(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object( 'course_id', course_id, 'student', student_username, 'assignment_id', assignment_id, 'course_name', course_name, 'title', title, 'content', content, 'due_date', due_date, 'total_points', points)) FROM assignments join courses using (course_id) where instructor_username=" + "'" + username + "'")
    rows = cur.fetchall()
    return rows

# get all of a teacher's assignments for a particular course
def get_teachers_assignments_for_course(username, course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object( 'course_name', course_name, 'title', title, 'content', content, 'points_received', grade, 'total_points', points, 'due_date', due_date, 'date_submitted', date_submitted)) FROM assignments join courses using (course_id) join grades using(assignment_id) where (instructor_username=" + "'" + username + "' and course_id=" + str(course_id) + ")")
    rows = cur.fetchall()
    return rows    

# get all of a student's courses
def get_students_courses(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    # cur.execute("SELECT * from courses join takes_course using (course_id) where username=" + "'" + username + "'")
    # return cur.fetchall()
    cur.execute("SELECT json_group_array( json_object( 'course_id', course_id, 'course_name', course_name, 'instructor_username', instructor_username)) FROM courses join takes_course using(course_id) where username=" + "'" + username + "'")
    rows = cur.fetchall()
    return rows

# get all of a student's grades + assignments for a particular course id
def get_students_grades_for_course(username, course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object('student', student_username, 'assignment_id', assignment_id, 'name', name, 'title', title, 'content', content, 'points_received', grade, 'total_points', points, 'due_date', due_date, 'date_submitted', date_submitted, 'submission', submission)) FROM assignments join grades using (assignment_id) join users where (username=" + "'" + username + "' and course_id=" + str(course_id) + ")")
    rows = cur.fetchall()
    return rows

# get ALL GRADES  for course
def get_all_students_grades_for_course(course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object('assignment_id', assignment_id, 'student', student_username, 'title', title, 'content', content, 'points_received', grade, 'total_points', points, 'due_date', due_date, 'date_submitted', date_submitted, 'submission', submission)) FROM assignments join grades using (assignment_id) where course_id=" + str(course_id))
    rows = cur.fetchall()
    return rows

# print(str(get_students_grades_for_course('patrick_whalen', 1)))
# print(str(get_all_students_grades_for_course(1)))

# TEST printing
# print('USERS:' + str(get_users()) + '\n')
# print('ANNOUNCEMENTS:' + str(get_announcements()) + '\n')
# print('COURSES:' + str(get_courses() )+ '\n')
# print('TAKES COURSE:' + str(get_takes_course()) + '\n')

# print('GERRY TEACHES COURSE:' + str(get_teachers_courses('gerry1954'))+'\n')
# print('Kat Takes COURSE:' + str(get_students_courses('patrick_whalen') )+'\n')
# print("ASSIGNMENTS:" + str(get_assignments()) + '\n')
# print("GRADES:" + str(get_grades()) + '\n')
# print("COURSE_ID 1 ANNOUNCEMENTS:" + str(get_announcements_course_id(1)) + '\n')
# print("COURSE_ID 1 ASSIGNMENTS:" + str(get_assignments_course_id(1)))
# print("Patrick grades for Mobile Dev: " + str(get_students_grades_for_course('patrick_whalen', 1)))
# print("Brady assignments for Algorithms: " + str(get_teachers_assignments_for_course('gerry1954', 4)))
# print("Brady assignments: " + str(get_teachers_assignments('gerry1954')))


# INSERTING DATA
def add_user(username, role, password, name, status, user_id, sq1, sq1_answer, sq2, sq2_answer, sq3, sq3_answer):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(cmd, (username, role, password, name, status, user_id, sq1, sq1_answer, sq2, sq2_answer, sq3, sq3_answer))
    conn.commit()
    return str("Successfully added user " + username)

# drop user (TESTING ONLY)
def drop_user(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "DELETE FROM users WHERE username=?"
    cur.execute(cmd, (username,))
    conn.commit()
    return str("User " + username + " dropped")

def add_announcement(course_id, title, content):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "INSERT INTO announcements (course_id, title, content, date_posted) VALUES(?, ?, ?, ?)"
    now = datetime.datetime.now()
    cur.execute(cmd, (str(course_id), title, content, now.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    return str("Successfully added an announcement")

# print("Adding a test user: " + str(add_user('vmisham', 'student', 'apollo', 'Vera Misham', 'poison', 'atroquinine', 'art', 'forgery', 'guilty', 'no')))
# print("Dropping user for debug: " + str(drop_user('vmisham')))
# print("Test annoucement: ", add_announcement(1, "test", "lorem_ipsum"))


# assign a student a grade
def grade_assignment(student, assignment_id, grade):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "UPDATE grades SET grade=? WHERE (student_username=? and assignment_id=?)"
    cur.execute(cmd, (grade, student, assignment_id))
    conn.commit()

# add assignment
def add_assignment(course_id, title, content, points, due_date):
    print("adding assignment")
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "INSERT INTO assignments VALUES(null, ?,?,?,?,?)"
    cur.execute(cmd, (course_id, title, content, points, due_date))
    conn.commit()
    cur.execute("SELECT assignment_id from assignments order by assignment_id desc limit 1")
    new_assignment = cur.fetchall()[0][0]
    print(new_assignment)
    # for all students in course_id, add new assignment
    students_in_course = cur.execute("SELECT username from takes_course where course_id=" + course_id).fetchall()
    # print(str(students_in_course))
    for row in students_in_course:
        student = row[0]
        cmd = "INSERT INTO grades VALUES(?,?, '', '', '' )"
        cur.execute(cmd, (new_assignment, student))
        conn.commit()
    # print(str(get_all_students_grades_for_course(course_id)))
    # print("\n"+"PRINTING ASSIGNMENTS:" + str(cur.fetchall()))
    return str("Successfully added assignment ")

def submit_assignment(assignment_id, student, submission):
    print(assignment_id)
    print(student)
    print(submission)
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    now = datetime.datetime.now()
    cmd = "UPDATE grades SET date_submitted=? WHERE (student_username=? and assignment_id=?)"
    cur.execute(cmd, (now.strftime('%Y-%m-%d %H:%M:%S'), student, assignment_id))
    conn.commit()
    cmd = "UPDATE grades SET submission=? WHERE (student_username=? and assignment_id=?)"
    cur.execute(cmd, (submission, student, assignment_id))
    conn.commit()
    return str('Successfully submitted assignment' + assignment_id + "for user " + student)

def get_assignment_by_name_student(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object('assignment_id', assignments.assignment_id, 'course_id', courses.course_id,'course_name', course_name, 'title', title, 'content', content, 'points', points, 'due_date', due_date)) FROM users JOIN assignments JOIN courses JOIN grades where (username=" + "'" + username + "' and role='student')")
    rows = cur.fetchall()
    return rows

def get_assignment_by_name_teacher(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object('assignment_id', assignments.assignment_id, 'course_id', courses.course_id, 'course_name', course_name, 'title', title, 'content', content, 'points', points, 'due_date', due_date, 'student_username', student_username, 'date_submitted', date_submitted, 'grade', grade)) FROM users JOIN assignments JOIN courses JOIN grades where (username=" + "'" + username + "' and role='instructor')")
    rows = cur.fetchall()
    return rows

# print("Test getting assignments (teacher):", get_assignment_by_name_teacher('gerry1954'))
# print("Test getting assignments (student):", get_assignment_by_name_student('patrick_whalen'))

def update_security_question(username, question_index, new_question, new_answer):
    if question_index == "1":
        cmd = 'UPDATE users SET sq1=?, sq1_answer=? WHERE username=?'
        conn = create_connection('canvas.db')
        cur = conn.cursor()
        cur.execute(cmd, (new_question, new_answer, username))
        conn.commit()
    elif question_index == "2":
        cmd = 'UPDATE users SET sq2=?, sq2_answer=? WHERE username=?'
        conn = create_connection('canvas.db')
        cur = conn.cursor()
        cur.execute(cmd, (new_question, new_answer, username))
        conn.commit()
    elif question_index == "3":
        cmd = 'UPDATE users SET sq3=?, sq3_answer=? WHERE username=?'
        conn = create_connection('canvas.db')
        cur = conn.cursor()
        cur.execute(cmd, (new_question, new_answer, username))
        conn.commit()
    else:
        # fail gracefully
        pass