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
    cur.execute("SELECT json_group_array( json_object( 'username', username, 'role', role, 'password', password, 'name', name ) ) FROM users")
    rows = cur.fetchall()
    return rows

def get_user_role(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users where username=" + "'" + username + "'")
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

# todo: get all grades by username
def get_grades_username():
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
    cur.execute("SELECT json_group_array( json_object( 'course_name', course_name, 'title', title, 'content', content, 'due_date', due_date)) FROM assignments join courses using (course_id) where instructor_username=" + "'" + username + "'")
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

# get all of a student's grades for a particular course id
def get_students_grades_for_course(username, course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object('assignment_id', assignment_id, 'name', name, 'title', title, 'content', content, 'points_received', grade, 'total_points', points, 'due_date', due_date, 'date_submitted', date_submitted)) FROM assignments join grades using (assignment_id) join users where (username=" + "'" + username + "' and course_id=" + str(course_id) + ")")
    rows = cur.fetchall()
    return rows

# get all grades for a course
def get_all_students_grades_for_course(course_id):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT json_group_array( json_object('assignment_id', assignment_id, 'student', student_username, 'title', title, 'content', content, 'points_received', grade, 'total_points', points, 'due_date', due_date, 'date_submitted', date_submitted)) FROM assignments join grades using (assignment_id) where course_id=" + str(course_id))
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
print("Patrick grades for Mobile Dev: " + str(get_students_grades_for_course('patrick_whalen', 1)))
# print("Brady assignments for Algorithms: " + str(get_teachers_assignments_for_course('gerry1954', 4)))
# print("Brady assignments: " + str(get_teachers_assignments('gerry1954')))


# INSERTING DATA
def add_user(username, role, password, name, sq1, sq1_answer, sq2, sq2_answer, sq3, sq3_answer):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(cmd, (username, role, password, name, sq1, sq1_answer, sq2, sq2_answer, sq3, sq3_answer))
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

# UPDATE DATA

# assign a student a grade
def grade_assignment(student, assignment_id, grade):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "UPDATE grades SET grade=? WHERE (student_username=? and assignment_id=?)"
    cur.execute(cmd, (grade, student, assignment_id))
    conn.commit()

# add assignment
def add_assignment(course_id, title, content, points, due_date):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cmd = "INSERT INTO assignments VALUES(null, ?,?,?,?,?)"
    cur.execute(cmd, (course_id, title, content, points, due_date))
    conn.commit()
    cur.execute("SELECT assignment_id from assignments order by assignment_id desc limit 1")
    print(cur.fetchall())
    return str("Successfully added assignment ")
    