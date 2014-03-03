#do some stuff with the db and a message queue here
from datetime import datetime as time
import config
def dbQ(queue, db):
    f = open(('database/logfile_db_' + str(pid)), 'w')
    while(True):
        dbEntry = queue.get(True);
        if len(dbEntry) == 3:
            db.execute('INSERT INTO users ' +
                       'VALUES (?,?,?,?);', dbEntry)
            f.write("User inserted: " + str(dbEntry) + " at " + str(time.now())) 
        elif len(dbEntry) == 4:
            db.execute('INSERT INTO notes (username, rebloggedFrom, PostID, type) ' +
                       'VALUES (?,?,?,?);', dbEntry)
            f.write("Note inserted: " + str(dbEntry) + " at " + str(time.now())) 
        elif len(dbEntry) == 6:
            db.execute('INSERT INTO posts ' +
                       'VALUES (?,?,?,?);', dbEntry)
            f.write("Post inserted: " + str(dbEntry) + " at " + str(time.now())) 
        else:
            f.write("Unrecognized entry type: " + str(dbEntry) + " at " + str(time.now())) 
        db.commit()

