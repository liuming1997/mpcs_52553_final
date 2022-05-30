import sqlite3
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
def get_announcements_course_id():
    pass

# get all grades
def get_grades():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT json_group_array( json_object( 'assignment_id', assignment_id, 'student_username', student_username, 'grade', grade) ) FROM grades")
    rows = cur.fetchall()
    return rows

# get all grades by username
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

# get all of a student's courses
def get_students_courses(username):
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    # cur.execute("SELECT * from courses join takes_course using (course_id) where username=" + "'" + username + "'")
    # return cur.fetchall()
    cur.execute("SELECT json_group_array( json_object( 'course_id', course_id, 'course_name', course_name, 'instructor_username', instructor_username)) FROM courses join takes_course using(course_id) where username=" + "'" + username + "'")
    rows = cur.fetchall()
    return rows

# TEST printing
# print('USERS:' + str(get_users()) + '\n')
# print('ANNOUNCEMENTS:' + str(get_announcements()) + '\n')
# print('COURSES:' + str(get_courses() )+ '\n')
# print('TAKES COURSE:' + str(get_takes_course()) + '\n')

# print('GERRY TEACHES COURSE:' + str(get_teachers_courses('gerry1954'))+'\n')
# print('Kat Takes COURSE:' + str(get_students_courses('patrick_whalen') )+'\n')
print("ASSIGNMENTS:" + str(get_assignments()) + '\n')
print("GRADES:" + str(get_grades()) + '\n')

# INSERTING DATA
def add_user():
    pass

def add_announcement():
    pass

# UPDATE DATA