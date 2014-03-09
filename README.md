Current status:
Probably working.  820 to 110 with 2500 still builds up a massive queue.  Hundreds of millions of lost entries.

division of labor:

main.py acts as a shared memory management server.  It has charge of three data structures shared between processes, enumerated as follows.

userDeck - this queue contains a list of users for the userCrawl function to operate on.

usersSeen - this dictionary holds the list of all users that have ever been added to userDeck.  Prevents multiple reads on the same user.

dataQ - this queue holds tuples of size 3, 4, or 6.  Depending on the tuple length, those tuples may represent data about users, notes, or posts.  Tuples are added to the queue by userCrawl, and removed from the queue by dbQ, which subsequently adds them to the database.


souplib.py holds the crawler.  It's horrible and needs to be rebased, but that's neither here nor there.  It crawls over a name, adding more names to userDeck (and usersSeen) if they aren't already in usersSeen.  It foists off reposts onto the crawler instance that handles the original poster.

dbQ.py handles database queries.  It pulls items off of dataQ, and inserts them into the database.  Each instance of dbQ running happens to have its own database.

joiner.py  - and on the subject of databases: this will merge all of the databases into one complete database.

start.pbs - run the whole thing via "qsub start.pbs", this script handles job management details over ACISS.
