# /usr/bin/python3
import time
from souplib import crawlUser
from dbQ import dbQ
import multiprocessing
import fileinput
import signal

manager = multiprocessing.Manager()
dbEnd = manager.Value('i', 0)
crawlEnd = manager.Value('i', 0)

def signal_term_handler(signal, frame):
    print("Terminating child processes")
    global crawlEnd
    global dbEnd
    crawlEnd.value = 1
    time.sleep(10)
    dbEnd.value = 1
    time.sleep(2)
    sys.exit(0)
         

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

    global manager
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
    signal.signal(signal.SIGTERM, signal_term_handler)
    for proc in ls:
        proc.join()

            
def main():
    f1()

if __name__ == '__main__':
    main()
