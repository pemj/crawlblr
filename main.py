# /usr/bin/python3
import time
from souplib import crawlUser
from dbQ import dbQ
import multiprocessing


#finds more users, adds user, post, and note info
def userize(userDeck, usersSeen, dataQ, debug):
    while(1):        
        if(userDeck):
            result = crawlUser(userDeck, usersSeen, dataQ, debug)
        else: 
            time.sleep(1)

#wraps a call to dbQ.  Stub functionality for now.
def dataEntry(dataDeck, debug):
    while(True):
        if dbQ:
            dbQ(dataDeck, debug)
        else:
            time.sleep(5)


def f1():
    #degree of multiprocessing
    degreeDB = 4
    degreeCrawl=55

    manager = multiprocessing.Manager()
    userDeck = manager.Queue()
    databaseQ = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    ls = []
    for i in range(0, degreeCrawl):
        ls.append(multiprocessing.Process(target=userize, args=(userDeck, usersSeen, databaseQ, True)))
        ls[i].start()
    for j in range(degreeCrawl, (degreeDB+degreeCrawl)):
        ls.append(multiprocessing.Process(target=dataEntry, args=(databaseQ, False)))
        ls[j].start()        
    for proc in ls:
        proc.join()
            
def main():
    f1()

if __name__ == '__main__':
    main()
