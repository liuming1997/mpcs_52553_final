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