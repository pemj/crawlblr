This readme serves as a brief introduction to the tumblr crawler 
project found in this repository.  The crawler itself is functional, 
though the code found in souplib.py could use some major refactoring.  
Note: in main.py, there are two variables that control the degree of 
multiprocessing: you're going to want to mess with those to your 
satisfaction.  We have found that 512 crawler instances and 200 
database workers perform adequately on a 12-core Intel Xeon computing 
node, but those numbers are massive overkill unless your system happens 
to have severe latency issues and a remarkably slow disk drive, or also 
happens to be very very beefy.

For a more rigorous description of dbQ.py and crawltech.py, see Section 
III in the related research paper.


division of labor:


The crawlblr folder holds crawltech.py, dbQ.py, models.py, and main.py


main.py acts as a shared memory management server.  It has charge of 
three data structures shared between processes, enumerated as follows.

    userDeck - this queue contains a list of users for the userCrawl 
    function to operate on.  Every new user we see gets added to this 
    for future observation.

    usersSeen - this dictionary holds the list of all users that have ever 
    been added to userDeck.  Prevents multiple reads on the same user.

    dataQ - this queue holds tuples of size 3, 4, or 6.  Depending on the 
    tuple length, those tuples may represent data about users, notes, or 
    posts.  Tuples are added to the queue by userCrawl, and removed from 
    the queue by dbQ, which subsequently adds them to the database.


crawltech.py holds the crawler. When supplies with a blog namee and the 
structures enumerates previously, it will feed data back to the 
database worker.  It first iterates over all posts from the given user, 
then registers all likes from that user.  When it encounters a repost 
among the original content, it will register it as a reblog and add the 
source of that reblog to the queue to be crawled by a future instance.

dbQ.py handles database queries.  It pulls items off of dataQ, and 
inserts them into the database.  Each instance of dbQ running happens 
to have its own database.

joiner.py  - and on the subject of databases: this will merge all 
of the databases into one complete database.



The pbs folder contains .pbs files, designed to launch the jobs via the 
ACISS job system.

start.pbs - run the whole thing via "qsub start.pbs", this script 
handles job management details over ACISS.
