import sqlite3
conn = sqlite3.connect('canvas.db')
c = conn.cursor()


# users table
c.execute('''
         CREATE TABLE users (
             username character varying(50) NOT NULL PRIMARY KEY ,
             role character NOT NULL,
             password TEXT NOT NULL,
             name character NOT NULL,
             sq1 character varying(50) NOT NULL,
             sq1_answer character varying(50) NOT NULL,
             sq2 character varying(50) NOT NULL,
             sq2_answer character varying(50) NOT NULL,
             sq3 character varying(50) NOT NULL,
             sq3_answer character varying(50) NOT NULL
         )
          ''')

# courses table
c.execute('''
          CREATE TABLE courses (
              course_id INTEGER PRIMARY KEY AUTOINCREMENT,
              course_name character varying(50),
              instructor_username character,
              FOREIGN KEY (instructor_username) REFERENCES users(username)
          )
          ''')


# announcements table
c.execute('''
          CREATE TABLE announcements (
                announcement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER,
                title character NOT NULL,
                content TEXT NOT NULL,
                date_posted DATETIME,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
          )
          ''')

# take course table
c.execute('''
          CREATE TABLE takes_course (
                username character, 
                course_id INTEGER, 
                FOREIGN KEY (course_id) REFERENCES courses(course_id), 
                FOREIGN KEY (username) REFERENCES users(username),
                PRIMARY KEY (username, course_id)
          )
          ''')

# assignments table
# todo: construct assignments table
c.execute('''
          CREATE TABLE assignments (
              assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
              course_id INTEGER,
              title character NOT NULL,
              content TEXT NOT NULL,
              due_date DATETIME NOT NULL,
              FOREIGN KEY (course_id) REFERENCES courses(course_id)
          )
          ''')

# grades table
# todo: construct grades table
c.execute('''
          CREATE TABLE grades (
              grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
              assignment_id INTEGER,
              course_id INTEGER,
              student character NOT NULL,
              grade character NOT NULL,
              FOREIGN KEY (course_id) REFERENCES courses(course_id),
              FOREIGN KEY (student) REFERENCES users(name),
              FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id)
          )
          ''')

# add users to db
c.executescript('''
          INSERT INTO users VALUES('klh875', 'student', '12345', 'Katharine Hedlund', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          INSERT INTO users VALUES('ming_liu', 'student', '12345', 'Ming Liu', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          INSERT INTO users VALUES('patrick_whalen', 'student', '12345', 'Patrick Whalen', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          INSERT INTO users VALUES('gerry1954', 'instructor', '12345', 'Gerry Brady', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          INSERT INTO users VALUES('chelsea_troy', 'instructor', '12345', 'Chelsea Troy', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          INSERT INTO users VALUES('y_terry', 'instructor', '12345', 'Yosvany Terry', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          INSERT INTO users VALUES('rafi_a', 'instructor', '12345', 'Rafi Almhana', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          INSERT INTO users VALUES('z_shang', 'instructor', '12345', 'Zechao Shang', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          ''')
# add admin user to db
c.execute(
    '''INSERT INTO users VALUES('molly', 'admin', '12345', 'Molly Stoner', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');''')

# add courses to db
conn.executescript('''
        INSERT INTO courses VALUES(null, 'Intro to Mobile Dev', 'chelsea_troy');
         INSERT INTO courses VALUES(null, 'Algorithms', 'gerry1954');
         INSERT INTO courses VALUES(null, 'Web Dev', 'rafi_a');
         INSERT INTO courses VALUES(null, 'Advanced Algorithms', 'gerry1954');
         INSERT INTO courses VALUES(null, 'Intro to Python Programming', 'chelsea_troy');
         INSERT INTO courses VALUES(null, 'Databases', 'z_shang');
         INSERT INTO courses VALUES(null, 'Discrete Mathematics', 'gerry1954');
         INSERT INTO courses VALUES(null, 'Afro Cuban Rhythms', 'y_terry');
''')

# associate students with courses
c.executescript('''
          INSERT INTO takes_course VALUES('klh875', 3);
          INSERT INTO takes_course VALUES('ming_liu', 3);
          INSERT INTO takes_course VALUES('patrick_whalen', 3);
          INSERT INTO takes_course VALUES('klh875', 1);
          INSERT INTO takes_course VALUES('ming_liu', 1);
          INSERT INTO takes_course VALUES('patrick_whalen', 1);
          INSERT INTO takes_course VALUES('klh875', 2);
          INSERT INTO takes_course VALUES('ming_liu', 2);
          INSERT INTO takes_course VALUES('patrick_whalen', 2);
          INSERT INTO takes_course VALUES('klh875', 4);
          INSERT INTO takes_course VALUES('ming_liu', 4);
          INSERT INTO takes_course VALUES('patrick_whalen', 4);
          INSERT INTO takes_course VALUES('klh875', 5);
          INSERT INTO takes_course VALUES('ming_liu', 5);
          INSERT INTO takes_course VALUES('patrick_whalen', 5);
          INSERT INTO takes_course VALUES('klh875', 6);
          INSERT INTO takes_course VALUES('ming_liu', 6);
          INSERT INTO takes_course VALUES('patrick_whalen', 6);
          INSERT INTO takes_course VALUES('klh875', 7);
          INSERT INTO takes_course VALUES('ming_liu', 7);
          INSERT INTO takes_course VALUES('patrick_whalen', 7);
          INSERT INTO takes_course VALUES('klh875', 8);
          ''')


# add data to announcements

# course_id, title_ content, dateposted

# add data to grade

# add data to assignments

conn.commit()