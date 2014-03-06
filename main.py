# /usr/bin/python3
import time
from souplib import crawlUser
from dbQ import dbQ
import multiprocessing


#finds more users, adds user, post, and note info
def userize(userDeck, usersSeen, dataQ, end, debug):
    while(True):        
        if end.value:
            return
        if(userDeck):
            result = crawlUser(userDeck, usersSeen, dataQ, end, debug)
        else: 
            time.sleep(1)

#wraps a call to dbQ.  Stub functionality for now.
def dataEntry(dataDeck, end, debug):
    while(True):
        if end.value:
            return
        if dbQ:
            dbQ(dataDeck, end, debug)
        else:
            time.sleep(5)


def f1():
    #degree of multiprocessing
    degreeDB = 2
    degreeCrawl=10

    manager = multiprocessing.Manager()
    dbEnd = manager.Value('i', 0)
    crawlEnd = manager.Value('i', 0)
    userDeck = manager.Queue()
    databaseQ = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    ls = []
    for i in range(0, degreeCrawl):
        ls.append(multiprocessing.Process(target=userize, args=(userDeck, usersSeen, databaseQ, crawlEnd, True)))
        ls[i].start()
    for j in range(degreeCrawl, (degreeDB+degreeCrawl)):
        ls.append(multiprocessing.Process(target=dataEntry, args=(databaseQ, dbEnd, True)))
        ls[j].start() 
    #end gracefully
    exiting=input("enter to kill program")
    print("Caught keyboard, sending shutdown signal to workers")
    crawlEnd.value = 1
    time.sleep(10)
    dbEnd.value = 1
    time.sleep(2)
    #for proc in ls:
    #    proc.join()
    return

            
def main():
    f1()

if __name__ == '__main__':
    main()
