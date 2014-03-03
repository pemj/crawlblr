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
    while(1):        
        if(userDeck):
            f.write(userDeck.get())
            userDeck.put("name"+str(num)+"\n")
            userDeck.put("name2"+str(num)+"\n")
            dataQ.put("wakka wakka"+"\n")
            time.sleep(1)
        else: 
            userDeck.put("failure")
            f.write("fail\n")
            time.sleep(5)

#actual function, takes in a list of users to visit and users visited
#finds more users, adds user, post, and note info
def userize(userDeck, usersSeen, dataQ, debug):
    while(1):        
        if(userDeck):
            result = crawlUser(userDeck, usersSeen, dataQ, debug)
        else: 
            time.sleep(2)

#wraps a call to dbQ.  Stub functionality for now.
def dataEntry(dataDeck):
    while(True):
        time.sleep(5)
        dbQ(dataDeck, 1)
        time.sleep(10)


def f1():
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)
    manager = multiprocessing.Manager()
    userDeck = manager.Queue()
    databaseQ = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    pool = multiprocessing.Pool(processes=degree)
    pool.apply_async(dataEntry, [databaseQ])
    for (i) in range(1,(degree-1)):
        #the True is for debugging.  Pass False when we're finished
        pool.apply_async(userize1, [userDeck, databaseQ, i])#usersSeen, databaseQ, True])
    pool.close()
    pool.join()

            
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
