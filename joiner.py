#!/usr/bin/python3
import subprocess
import re
import sqlite3

#remove the final if we have it
os.unlink('final.db')

#fill the list of database filenames, dbFiles
output, error= subprocess.Popen(["ls"], stdout=subprocess.PIPE).communicate()
filePattern = re.compile('^[a-z0-9A-Z_]+(\.db)+$')
li = [x.decode('utf-8') for x in output.split(b'\n')]
dbFiles = [x for x in li if filePattern.match(x)]

#initialize the destination database
conn = sqlite3.connect('final.db')
c = conn.cursor()
c.execute('''create table if not exists users
(username text, lastUpdated text, postCount integer)''')
c.execute('''create table if not exists posts
(username text, postID text, type text, date text, noteCount integer)''')
c.execute('''create table if not exists notes
(username text, rebloggedFrom text, postID text, type text)''')
conn.commit()

#for each database:
for base in dbFiles:
    #attach to that database
    c.execute('''attach ? as toMerge''', (base,))
    #add all of its rows to the final database
    c.execute('''insert into users select * from toMerge.users''')
    c.execute('''insert into posts select * from toMerge.posts''')
    c.execute('''insert into notes select * from toMerge.notes''')
    #detach from that database
    c.execute('''detach toMerge''')
    #finalize the changes
    conn.commit()
#close our connection, we're done.
c.close()


print(dbFiles)
