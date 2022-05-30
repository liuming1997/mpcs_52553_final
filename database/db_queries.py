import sqlite3

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
    print("insert called")

# get all users
def get_users():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT * from users")
    rows = cur.fetchall()
    return rows

# get all courses
def get_courses():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT * from courses")
    rows = cur.fetchall()
    return rows

# get all announcements
def get_announcements():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT * from announcements")
    rows = cur.fetchall()
    return rows

def get_teaches_course():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT * from teaches_course")
    rows = cur.fetchall()
    return rows

def get_takes_course():
    conn = create_connection('canvas.db')
    cur = conn.cursor()
    cur.execute("SELECT * from takes_course")
    rows = cur.fetchall()
    return rows

# BASIC TEST printing
# print(str(get_users()) + '\n')
# print(str(get_announcements()) + '\n')
# print(str(get_courses() )+ '\n')
# print(str(get_takes_course()) + '\n')
# print(str(get_teaches_course() )+'\n')
