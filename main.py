# /usr/bin/python3
from urllib import request
#from importer import import_path
#import_path("beautifulsoup/bs4")
from bs4 import BeautifulSoup
from collections import deque
import re
import time
import sqlite3
from souplib import crawlUser
from dbQ import dbQ
import multiprocessing
degreeDB = 4
degreeCrawl=55

#multiprocess functionaliy checking        
def userize1(userDeck, dataQ, num):
    f = open(("logfile_" + str(num)), "w")
    f.write("begin")
    while(True):        
        f.write(userDeck.get())
        userDeck.put("name1_"+str(num)+"\n")
        userDeck.put("name2_"+str(num)+"\n")
        dataQ.put("wakka wakka"+"\n")
    f.close()
#actual function, takes in a list of users to visit and users visited
#finds more users, adds user, post, and note info
def userize(userDeck, usersSeen, dataQ, debug):
    while(1):        
        if(userDeck):
            result = crawlUser(userDeck, usersSeen, dataQ, debug)
        else: 
            time.sleep(1)

#wraps a call to dbQ.  Stub functionality for now.
def dataEntry(dataDeck, debug):
    time.sleep(5)
    while(True):
        if dbQ:
            dbQ(dataDeck, debug)
        else:
            time.sleep(5)


def f1():
    manager = multiprocessing.Manager()
    userDeck = manager.Queue()
    databaseQ = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    ls = []
    for i in range(0, degreeCrawl):
        ls.append(multiprocessing.Process(target=userize, args=(userDeck, usersSeen, databaseQ, True)))
        #ls.append(multiprocessing.Process(target=userize1, args=(userDeck, databaseQ, i)))
        ls[i].start()
    for j in range(degreeCrawl, (degreeDB+degreeCrawl)):
        ls.append(multiprocessing.Process(target=dataEntry, args=(databaseQ, False)))
        ls[j].start()        
    for proc in ls:
        proc.join()

            
def main():
    
    conn = sqlite3.connect('database/weekday.db')
    c = conn.cursor()
    #c.execute('''PRAGMA journal_mode = OFF''')
    c.execute('''create table if not exists users
    (username text, lastUpdated text, postCount integer)''')
    c.execute('''create table if not exists posts
    (poster text, source text, postID text, type text, date text, noteCount integer)''')
    c.execute('''create table if not exists notes
    (username text, rebloggedFrom text, postID text, type text)''')
    conn.commit()
    c.close()
    f1()

if __name__ == '__main__':
    main()
