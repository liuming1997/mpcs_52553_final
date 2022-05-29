import sqlite3
conn = sqlite3.connect('canvas.db')
c = conn.cursor()


# users table
c.execute('''
         CREATE TABLE users (
             username character varying(50) NOT NULL PRIMARY KEY ,
             role character NOT NULL,
             password TEXT NOT NULL,
             name character NOT NULL
         )
          ''')

# courses table
c.execute('''
          CREATE TABLE courses (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              course_name character varying(50),
              instructor_username character,
              instructor_name character,
              FOREIGN KEY (instructor_username) REFERENCES users(username),
              FOREIGN KEY (instructor_name) REFERENCES users(name)
          )
          ''')

# teaches course table
# links courses to people enrolled in or teaching that course
c.execute('''
          CREATE TABLE takes_course (
                username character,
                course_id INTEGER, 
                FOREIGN KEY (course_id) REFERENCES courses(id),
                FOREIGN KEY (username) REFERENCES users(username),
                PRIMARY KEY (course_id, username)
          )
          ''')

# takes course table
c.execute('''
          CREATE TABLE teaches_course (
                username character,
                course_id INTEGER, 
                FOREIGN KEY (course_id) REFERENCES courses(id),
                FOREIGN KEY (username) REFERENCES users(username),
                PRIMARY KEY (course_id)
          )
          ''')

# announcements table
c.execute('''
          CREATE TABLE announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT ,
                course_id INTEGER,
                title character NOT NULL,
                author character,
                content TEXT NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(id),
                FOREIGN KEY (author) REFERENCES users(name)
          )
          ''')


# assignments table
# todo: construct assignments table

# grades table
# todo: construct grades table

# add users to db
c.executescript('''
          INSERT INTO users VALUES('klh875', 'student', '12345', 'Katharine Hedlund');
          INSERT INTO users VALUES('ming_liu', 'student', '12345', 'Ming Liu');
          INSERT INTO users VALUES('patrick_whalen', 'student', '12345', 'Patrick Whalen');
          INSERT INTO users VALUES('gerry1954', 'instructor', '12345', 'Gerry Brady');
          INSERT INTO users VALUES('chelsea_troy', 'instructor', '12345', 'Chelsea Troy');
          INSERT INTO users VALUES('t_terry', 'instructor', '12345', 'Yosvany Terry');
          ''')


# add courses to db
conn.executescript('''
        INSERT INTO courses VALUES(null, 'Intro to Mobile Dev', 'Chelsea Troy', 'chelsea_troy');
         INSERT INTO courses VALUES(null, 'Algorithms', 'Gerry Brady', 'gerry1954');
         INSERT INTO courses VALUES(null, 'Web Dev', 'Rafi Almhana', 'rafi_a');
         INSERT INTO courses VALUES(null, 'Advanced Algorithms', 'Gerry Brady', 'gerry1954');
         INSERT INTO courses VALUES(null, 'Intro to Python Programming', 'Chelsea Troy', 'chelsea_troy');
         INSERT INTO courses VALUES(null, 'Databases', 'Zechao Shang', 'z_shang');
         INSERT INTO courses VALUES(null, 'Discrete Mathematics', 'Gerry Brady', 'gerry1954');
         INSERT INTO courses VALUES(null, 'Afro Cuban Rhythms', 'Yosvany Terry', 'y_terry');
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
          INSERT INTO takes_course VALUES('ming_liu', 8);
          INSERT INTO takes_course VALUES('patrick_whalen', 8);
          ''')

# associate instructors with courses
c.executescript('''
          INSERT INTO teaches_course VALUES('chelsea_troy', 1);
          INSERT INTO teaches_course VALUES('gerry1954', 2);
          INSERT INTO teaches_course VALUES('rafi_a', 3);
          INSERT INTO teaches_course VALUES('gerry1954', 4);
          INSERT INTO teaches_course VALUES('chelsea_troy', 5);
          INSERT INTO teaches_course VALUES('z_shang', 6);
          INSERT INTO teaches_course VALUES('gerry1954', 7);
          INSERT INTO teaches_course VALUES('y_terry', 8);
          ''')

# add data to announcements

conn.commit()