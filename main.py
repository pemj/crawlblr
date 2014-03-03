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
degree=4

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
            time.sleep(2)

#wraps a call to dbQ.  Stub functionality for now.
def dataEntry(dataDeck, debug):
    time.sleep(5)
    while(True):
        if dbQ:
            dbQ(dataDeck, 1)
        else:
            time.sleep(5)


def f1():
    manager = multiprocessing.Manager()
    userDeck = manager.Queue()
    databaseQ = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    d = multiprocessing.Process(target=dataEntry, args=(databaseQ, 1))
    d.start()
    ls = []
    for i in range(degree):
        ls.append(multiprocessing.Process(target=userize, args=(userDeck, usersSeen, databaseQ, True)))
        #ls.append(multiprocessing.Process(target=userize1, args=(userDeck, databaseQ, i)))
        ls[i].start()
        time.sleep(2)
    for i in ls:
        i.join()

            
def main():
    
    conn = sqlite3.connect('database/weekday.db')
    c = conn.cursor()
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
