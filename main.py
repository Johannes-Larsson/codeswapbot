import praw
import sqlite3
import json
from praw.models import Message
from pprint import pprint
import messageMaker

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


# check new messages
for message in reddit.inbox.unread(limit=None):
    if isinstance(message, Message):
        print('new message from ' + message.author.name + ':')
        print(message.subject)
        print(message.body)
        if 'no' in message.body.lower() + message.subject.lower():
            message.mark_read()
            cursor.execute('delete from users where name = ?', (message.author.name,))
            db.commit()
            message.author.message('Code swap', messageMaker.declined())
        elif 'code swap' in message.body.lower() + message.subject.lower():
            message.mark_read()
            message.author.message('Code swap', messageMaker.firstContact())
            cursor.execute('insert into users (name, recieve_date) \
            values (:name, (select date()))',
            {'name':message.author.name})
            db.commit()

# pair people up
cursor.execute('select name, id from users where partner is null\
 order by recieve_date asc')
while True:
    user1 = cursor.fetchone()
    user2 = cursor.fetchone()
    if user1 == None or user2 == None:
        break
    else:
        r1 = reddit.redditor(user1[0])
        r2 = reddit.redditor(user1[0])

        print('new pair: ' + r1.name + ' and ' + r2.name)

        r2.message('Code swap', messageMaker.pair(r2.name))
        r2.message('Code swap', messageMaker.pair(r1.name))

        cursor.executemany('update users\
         set partner = ?, partnered_date = (select date()) where id = ?',
         [user1, user2])
        db.commit()
