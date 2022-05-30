import sqlite3

from numpy import append
conn = sqlite3.connect('canvas.db')
c = conn.cursor()

from faker import Faker
fake = Faker()
people = []
usernames = []
sq1 = []
sq1_answer = []
sq2 = []
sq2_answer = []
sq3 = []
sq3_answer = []

for _ in range(100):
    people.append(fake.name())
    usernames.append(fake.user_name())
    sq1.append(fake.sentence(nb_words=4))
    sq1_answer.append(fake.sentence(nb_words=4))
    sq2.append(fake.sentence(nb_words=5))
    sq2_answer.append(fake.sentence(nb_words=5))
    sq3.append(fake.sentence(nb_words=6))
    sq3_answer.append(fake.sentence(nb_words=6))

c.execute('''INSERT INTO users VALUES('molly', 'admin', '12345', 'Molly Stoner', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');''')

for i in range(len(people)):
    string = 'INSERT INTO users VALUES(\'' + usernames[i] + '\', \'student\', \'12345\', \'' +  people[i] + '\', \'' 
    string += sq1[i] + '\', \'' + sq1_answer[i] + '\', \'' + sq2[i] + '\', \'' + sq2_answer[i] + '\', \'' + sq3[i] + '\', \'' + sq3_answer[i] + '\');'
    c.execute(string)


string_2 = '${sq1[0]}, ${sq1_answer[0]}, ${sq2[0]}, ${sq2_answer[0]}, ${sq3[0]}, ${sq3_answer[0]}'
# add users to db
c.executescript('''
          INSERT INTO users VALUES('klh875', 'student', '12345', 'Katharine Hedlund', 'Yes', 'No', 'One', 'Two', 'Red', 'Blue');
          INSERT INTO users VALUES('ming_liu', 'student', '12345', 'Ming Liu', ${sq1[0]}, ${sq1_answer[0]}, ${sq2[0]}, ${sq2_answer[0]}, ${sq3[0]}, ${sq3_answer[0]});
          INSERT INTO users VALUES('patrick_whalen', 'student', '12345', 'Patrick Whalen', ${sq1[0]}, ${sq1_answer[0]}, ${sq2[0]}, ${sq2_answer[0]}, ${sq3[0]}, ${sq3_answer[0]});
          INSERT INTO users VALUES('gerry1954', 'instructor', '12345', 'Gerry Brady', ${sq1[0]}, ${sq1_answer[0]}, ${sq2[0]}, ${sq2_answer[0]}, ${sq3[0]}, ${sq3_answer[0]});
          INSERT INTO users VALUES('chelsea_troy', 'instructor', '12345', 'Chelsea Troy', ${sq1[0]}, ${sq1_answer[0]}, ${sq2[0]}, ${sq2_answer[0]}, ${sq3[0]}, ${sq3_answer[0]});
          INSERT INTO users VALUES('y_terry', 'instructor', '12345', 'Yosvany Terry', ${sq1[0]}, ${sq1_answer[0]}, ${sq2[0]}, ${sq2_answer[0]}, ${sq3[0]}, ${sq3_answer[0]});
          INSERT INTO users VALUES('rafi_a', 'instructor', '12345', 'Rafi Almhana', ${sq1[0]}, ${sq1_answer[0]}, ${sq2[0]}, ${sq2_answer[0]}, ${sq3[0]}, ${sq3_answer[0]});
          INSERT INTO users VALUES('z_shang', 'instructor', '12345', 'Zechao Shang', ${sq1[0]}, ${sq1_answer[0]}, ${sq2[0]}, ${sq2_answer[0]}, ${sq3[0]}, ${sq3_answer[0]});
          ''')

c.commit()
