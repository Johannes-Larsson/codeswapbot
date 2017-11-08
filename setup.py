import sqlite3
db = sqlite3.connect('data.db')
c=db.cursor()
c.execute('create table users (id integer primary key, name text, partner text, recieve_date date, partnered_date date)')
db.commit()
db.close()
