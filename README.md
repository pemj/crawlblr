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

For a more rigorous description of dbQ.py and souplib.py, see Section 
III in the attached research paper.

division of labor:

main.py acts as a shared memory management server.  It has charge of three data structures shared between processes, enumerated as follows.

userDeck - this queue contains a list of users for the userCrawl 
function to operate on.  Every new user we see gets added to this 
for future observation.

usersSeen - this dictionary holds the list of all users that have ever 
been added to userDeck.  Prevents multiple reads on the same user.

dataQ - this queue holds tuples of size 3, 4, or 6.  Depending on the 
tuple length, those tuples may represent data about users, notes, or 
posts.  Tuples are added to the queue by userCrawl, and removed from 
the queue by dbQ, which subsequently adds them to the database.


souplib.py holds the crawler.  It's horrible and needs to be refactored, 
but that's neither here nor there.  It crawls over a name, adding more 
names to userDeck (and usersSeen) if they aren't already in usersSeen.  
It foists off reposts onto the crawler instance that handles the 
original poster.

dbQ.py handles database queries.  It pulls items off of dataQ, and 
inserts them into the database.  Each instance of dbQ running happens 
to have its own database.

joiner.py  - and on the subject of databases: this will merge all 
of the databases into one complete database.

start.pbs - run the whole thing via "qsub start.pbs", this script 
handles job management details over ACISS.

latestUser.py - the latest version of one of the more interesting 
problems we encountered: the inference of following relationships 
from user->content relations.  This is the most efficient version, 
developed thus far, but it contains only a crude simulacrum of the 
algorithm identified in our paper.

but is still largely a mockup of the features that an
