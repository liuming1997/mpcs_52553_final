import sqlite3
from faker import Faker
import datetime
import random

conn = sqlite3.connect('canvas.db')
c = conn.cursor()

username = 'patrick_whalen'
password = '12345'

# classes to use: 2 and 3

fake = Faker()
now = datetime.datetime.now()
i = 1
cmd = "INSERT into announcements VALUES(null, 2, ?, ?, ?)"
while (i < 10):
    c.execute(cmd, ("Announcement " + str(i), fake.paragraph(nb_sentences=4, variable_nb_sentences=True) ,now.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    i += 1
j = 1
cmd = "INSERT into announcements VALUES(null, 3, ?, ?, ?)"
while (j < 15):
    c.execute(cmd, ("Announcement " + str(j), fake.paragraph(nb_sentences=7, variable_nb_sentences=True) ,now.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    j += 1
a = 1
cmd = "INSERT into assignments VALUES(null, 2, ?, ?, ?, ?)"
while (a < 15):
    c.execute(cmd, ("Assignment " + str(a), "Problem Set " + str(a), random.randint(50,100), fake.future_datetime()))
    conn.commit()
    a += 1
b = 1
cmd = "INSERT into assignments VALUES(null, 3, ?, ?, ?, ?)"
while (b < 20):
    c.execute(cmd, ("Assignment " + str(b), "Homework " + str(b), random.randint(10,20), fake.future_datetime()))
    conn.commit()
    b += 1