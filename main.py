# /usr/bin/python3
from urllib import request
from importer import import_path
#import_path("/home/users/pem/crawlblr/beautifulsoup/bs4")
from bs4 import BeautifulSoup
from collections import deque
import re
import time
import sqlite3
from souplib import crawlUser
import multiprocessing
degree=3

        
def userize1(userDeck, num):
    f = open(("logfile_" + str(num)), "w")
    while(1):        
        if(userDeck):
            f.write(userDeck.get())
            userDeck.put("name"+str(num))
            userDeck.put("name2"+str(num))
            time.sleep(1)
        else: 
            f.write("fail")
            time.sleep(5)

def userize(userDeck, usersSeen):
    while(1):        
        if(userDeck):
            result = crawlUser(userDeck, usersSeen)
        else: 
            time.sleep(2)



def f1():
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)
    manager = multiprocessing.Manager()
    userDeck = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    pool = multiprocessing.Pool(processes=degree)
    for (i) in range(0,3):
        pool.apply_async(userize1, [userDeck, i])# usersSeen])
    pool.close()
    pool.join()

            
def main():
    
    #conn = sqlite3.connect('/cs/groupprojects/cis632/pem/database/weekday.db')
    #c = conn.cursor()
    #c.execute('''create table users
    #               (username text, lastUpdated text, postCount integer)''')
    #c.execute('''create table posts
    #               (poster text, source text, postID text, type text, date text, noteCount integer)''')
    #c.execute('''create table notes
    #               (username text, rebloggedFrom text, postID text, type text)''')
    #conn.close()
    f1()

if __name__ == '__main__':
    main()
