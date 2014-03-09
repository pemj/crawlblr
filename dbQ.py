#do some stuff with the db and a message queue here
from datetime import datetime as time
import os
import sqlite3
from multiprocessing import Queue, Manager
from queue import Empty

def dbQ(crawlQ, num, end, debug):
    writesInBatch = 0;
    pid = os.getpid()
    #temporary while we figure out how to get the database sharing 
    #figured out
    conn = sqlite3.connect('database/weekday_' + str(pid) +'.db')
    db = conn.cursor()
    db.execute('''create table if not exists users
    (username text, lastUpdated text, postCount integer)''')
    db.execute('''create table if not exists posts
    (username text, postID text, type text, date text, noteCount integer)''')
    db.execute('''create table if not exists notes
    (username text, rebloggedFrom text, postID text, type text)''')
    conn.commit()
    #logging
    f = open(('database/logfile_db_' + str(pid)), 'w')
    if debug:
        f.write("dbQ start\n")
    
    while(True):
        if end.value < num:
            f.write("closing down database process " + str(pid)+"\n")
            conn.commit()
            db.close()
            f.close()
            return
        f.write("[DEBUG] Queue length = " + str(crawlQ.qsize()) + " for pid = " + str(pid) +" at time = " + str(time.now()) + "\n")
        try:
            dbEntry = crawlQ.get(True, 1);
        except Empty:
            continue
        if len(dbEntry) == 3:
            db.execute('INSERT INTO users ' +
                       'VALUES (?,?,?);', dbEntry)
            if debug: 
                f.write("[DEBUG] User inserted: " + str(dbEntry) + " at " + str(time.now())+"\n") 
            writesInBatch += 1
        elif len(dbEntry) == 4:
            db.execute('INSERT INTO notes (username, rebloggedFrom, PostID, type) ' +
                       'VALUES (?,?,?,?);', dbEntry)
            if debug:
                f.write("[DEBUG] Note inserted: " + str(dbEntry) + " at " + str(time.now())+"\n") 
            writesInBatch += 1
        elif len(dbEntry) == 5:
            db.execute('INSERT INTO posts ' +
                       'VALUES (?,?,?,?,?);', dbEntry)
            if debug:
                f.write("[DEBUG] Post inserted: " + str(dbEntry) + " at " + str(time.now())+"\n") 
            writesInBatch += 1
        else:
            f.write("[ERROR] Unrecognized entry type: " + str(dbEntry) + " at " + str(time.now())+ "\n") 
        #we commit to the database connection, not the cursor
        #so, at the minimum, we'll need to pass the connection
        if(writesInBatch >= 200):
            conn.commit()
            if debug:
                f.write("[DEBUG] Wrote " + str(writesInBatch) + " to the DB at " + str(time.now())+"\n") 
            writesInBatch = 0
        #we do close at the cursor though, so there's that.
    db.close()
