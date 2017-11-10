# codeswapbot
/r/todoist bot for getting users wanting to swap promo codes in touch.


Intended to declutter the subreddit that is constantly spammed with code swap threads.

# How it works
The script checks it's messages for ones containing 'code swap' in the title or body. Authors of those are added to the database.
If the message contains 'no' the user is removed from the database.

It then checks the database and pairs up people wanting to swap, sending them a message with their partner's username. 
The swap itself is made by the users themselves; the bot doesn't handle the codes.

# Installation
- install python (unless you have it installed already, which you probably do
- install pip and sqlite3 (````apt install python-pip sqlite3```` might work)
- ````pip install praw````
- ````python setup.py````

then you can
- ````python main.py````
