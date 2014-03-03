Current status:
seems to work.  We only have it running with one database worker, but it seems to be running okay.  We'll see how it actually runs on ACISS soon.

BELAY THAT
just ran into this guy:

crawlblr/dbQ.py", line 35, in dbQ
sqlite3.OperationalError: disk I/O error
I guess we can catch that error and retry?  Who knows what the hell this is all about though.


division of labor:

main.py acts as a shared memory management server.  It has charge of three data structures shared between processes, enumerated as follows.

userDeck - this queue contains a list of users for the userCrawl function to operate on.

usersSeen - this dictionary holds the list of all users that have ever been added to userDeck.  Prevents multiple reads on the same user.

dataQ - this queue holds tuples of size 3, 4, or 6.  Depending on the tuple length, those tuples may represent data about users, notes, or posts.  Tuples are added to the queue by userCrawl, and removed from the queue by dbQ, which subsequently adds them to the database.

Data structures we need to implement:

We need to add something that is shared between instances of dbQ, so that we can add and remove instances of that process as needed.