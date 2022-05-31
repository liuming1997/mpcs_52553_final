import sqlite3
conn = sqlite3.connect('canvas.db')
c = conn.cursor()


# users table
# todo: Add column for active or inactive! default is active
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
              points character NOT NULL,
              due_date DATETIME NOT NULL,
              FOREIGN KEY (course_id) REFERENCES courses(course_id)
          )
          ''')

# grades table
# todo: construct grades table
c.execute('''
          CREATE TABLE grades (
              assignment_id INTEGER,
              student_username character NOT NULL,
              grade character NOT NULL,
              date_submitted DATETIME,
              FOREIGN KEY (student_username) REFERENCES users(username),
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


# add data to announcements - algorithms
# course id: 1 instructor: gerry1954
# course_id, title_ content, dateposted
c.executescript('''
          INSERT INTO announcements VALUES(null, 1, 'Announcement 1',  'HW 1 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 2',  'HW 2 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 3',  'HW 3 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 4',  'HW 4 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 5',  'HW 5 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 6',  'Project 1 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 7',  'Midterm grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 8',  'Midterm Part 2 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 9',  'HW 6 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 10',  'HW 7 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 11',  'HW 8 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 12',  'HW 9 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 13',  'HW 10 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 14',  'Final exam grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 1, 'Announcement 15',  'Final grades are posted', (SELECT datetime('now')));
          ''')

# add announcements to advanced algos
c.executescript('''
          INSERT INTO announcements VALUES(null, 4, 'Announcement 1',  'HW 1 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 2',  'HW 2 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 3',  'HW 3 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 4',  'HW 4 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 5',  'HW 5 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 6',  'Project 1 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 7',  'Midterm grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 8',  'Midterm Part 2 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 9',  'HW 6 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 10',  'HW 7 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 11',  'HW 8 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 12',  'HW 9 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 13',  'HW 10 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 14',  'Final exam grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 4, 'Announcement 15',  'Final grades are posted', (SELECT datetime('now')));
          ''')

c.executescript('''
          INSERT INTO announcements VALUES(null, 7, 'Announcement 1',  'HW 1 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 2',  'HW 2 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 3',  'HW 3 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 4',  'HW 4 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 5',  'HW 5 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 6',  'Project 1 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 7',  'Midterm grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 8',  'Midterm Part 2 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 9',  'HW 6 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 10',  'HW 7 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 11',  'HW 8 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 12',  'HW 9 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 13',  'HW 10 grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 14',  'Final exam grades are posted', (SELECT datetime('now')));
          INSERT INTO announcements VALUES(null, 7, 'Announcement 15',  'Final grades are posted', (SELECT datetime('now')));
          ''')

# add data to assignments - algorithms
# null, course_id, title, content, points, due_date
c.executescript('''
          INSERT INTO assignments VALUES(null, 1, 'Assignment 1',  'HW 1 ', '100', (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 2',  'HW 2 ', '100', (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 3',  'HW 3 ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 4',  'HW 4 ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 5',  'Midterm ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 6',  'HW 7 ','100',  (SELECT datetime('now')));
          ''')
c.executescript('''
          INSERT INTO assignments VALUES(null, 4, 'Assignment 1',  'HW 1 ', '100', (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 4, 'Assignment 2',  'HW 2 ', '100', (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 4, 'Assignment 3',  'HW 3 ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 4, 'Assignment 4',  'HW 4 ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 4, 'Assignment 5',  'Midterm ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 4, 'Assignment 6',  'HW 7 ','100',  (SELECT datetime('now')));
          ''')

c.executescript('''
          INSERT INTO assignments VALUES(null, 1, 'Assignment 7',  'HW 1 ', '100', (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 7',  'HW 2 ', '100', (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 7',  'HW 3 ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 7',  'HW 4 ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 7',  'Midterm ','100',  (SELECT datetime('now')));
          INSERT INTO assignments VALUES(null, 1, 'Assignment 7',  'HW 7 ','100',  (SELECT datetime('now')));
          ''')

# add data to grades
# patrick_whalen account
c.executescript('''
          INSERT INTO grades VALUES(1, 'patrick_whalen', 5, (SELECT datetime('now')));
          INSERT INTO grades VALUES(2, 'patrick_whalen', 90, (SELECT datetime('now')));
          INSERT INTO grades VALUES(3, 'patrick_whalen', 80, (SELECT datetime('now')));
          INSERT INTO grades VALUES(4, 'patrick_whalen', 90, (SELECT datetime('now')));
          INSERT INTO grades VALUES(5, 'patrick_whalen', 50, (SELECT datetime('now')));
          INSERT INTO grades VALUES(6, 'patrick_whalen', 0, (SELECT datetime('now')));
          INSERT INTO grades VALUES(7, 'patrick_whalen', 5, (SELECT datetime('now')));
          INSERT INTO grades VALUES(8, 'patrick_whalen', 90, (SELECT datetime('now')));
          INSERT INTO grades VALUES(9, 'patrick_whalen', 80, (SELECT datetime('now')));
          INSERT INTO grades VALUES(10, 'patrick_whalen', 90, (SELECT datetime('now')));
          INSERT INTO grades VALUES(11, 'patrick_whalen', 50, (SELECT datetime('now')));
          INSERT INTO grades VALUES(12, 'patrick_whalen', 0, (SELECT datetime('now')));
          INSERT INTO grades VALUES(13, 'patrick_whalen', 5, (SELECT datetime('now')));
          INSERT INTO grades VALUES(14, 'patrick_whalen', 90, (SELECT datetime('now')));
          INSERT INTO grades VALUES(15, 'patrick_whalen', 80, (SELECT datetime('now')));
          INSERT INTO grades VALUES(16, 'patrick_whalen', 90, (SELECT datetime('now')));
          INSERT INTO grades VALUES(17, 'patrick_whalen', 50, (SELECT datetime('now')));
          INSERT INTO grades VALUES(18, 'patrick_whalen', 0, (SELECT datetime('now')));
          ''')

conn.commit()