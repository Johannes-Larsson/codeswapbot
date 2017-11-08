import praw
import sqlite3
import json
from pprint import pprint

with open('login.json') as login_info:
    login = json.load(login_info)

db = sqlite3.connect('data.db')
cursor = db.cursor()

reddit = praw.Reddit(client_id=login['clientId'],
        client_secret=login['clientSecret'],
        password=login['password'],
        user_agent=login['userAgent'],
        username=login['username'])

print('logged in as ' + str(reddit.user.me()))


for message in reddit.inbox.messages():
    if message.new:
        print('new message from ' + message.author.name + ':')
        print(message.subject)
        print(message.body)
        if 'code swap' in message.body.lower() + message.subject.lower():
            message.mark_read()
            cursor.execute('insert into users (name, recieve_date) values (:name, (select date()))',{'name':message.author.name})
            db.commit()
