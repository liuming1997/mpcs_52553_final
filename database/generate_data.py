import sqlite3

from numpy import append
conn = sqlite3.connect('canvas.db')
c = conn.cursor()

from faker import Faker
fake = Faker()
people = []
usernames = []

for _ in range(100):
    people.append(fake.name())
    usernames.append(fake.user_name())


c.execute('''INSERT INTO users VALUES('molly', 'admin', '12345', 'Molly Stoner');''')

for i in range(len(people)):
    string = 'INSERT INTO users VALUES(\'' + usernames[i] + '\', \'student\', \'12345\', \'' +  people[i] + '\');'
    c.execute(string)