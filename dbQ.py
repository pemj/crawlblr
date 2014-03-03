#do some stuff with the db and a message queue here
from datetime import datetime as time
import config
def dbQ(queue, db):
    #temporary while we figure out how to get the database sharing 
    #figured out
    conn = sqlite3.connect('database/weekday.db')
    db = conn.cursor()
    #logging
    f = open(('database/logfile_db_' + str(pid)), 'w')
    while(True):
        dbEntry = queue.get(True);
        if len(dbEntry) == 3:
            db.execute('INSERT INTO users ' +
                       'VALUES (?,?,?);', dbEntry)
            f.write("User inserted: " + str(dbEntry) + " at " + str(time.now())) 
        elif len(dbEntry) == 4:
            db.execute('INSERT INTO notes (username, rebloggedFrom, PostID, type) ' +
                       'VALUES (?,?,?,?);', dbEntry)
            f.write("Note inserted: " + str(dbEntry) + " at " + str(time.now())) 
        elif len(dbEntry) == 6:
            db.execute('INSERT INTO posts ' +
                       'VALUES (?,?,?,?,?,?);', dbEntry)
            f.write("Post inserted: " + str(dbEntry) + " at " + str(time.now())) 
        else:
            f.write("Unrecognized entry type: " + str(dbEntry) + " at " + str(time.now())) 
        #we commit to the database connection, not the cursor
        #so, at the minimum, we'll need to pass the connection
        conn.commit()
        #we do close at the cursor though, so there's that.
        db.close()