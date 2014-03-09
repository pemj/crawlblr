# /usr/bin/python3
import time
from souplib import crawlUser
from dbQ import dbQ
import multiprocessing
import fileinput
import signal

manager = multiprocessing.Manager()
dbEnd = manager.Value('i', 0)
crawlDeg = manager.Value('i', 0)

def signal_term_handler(signal, frame):
    print("Terminating child processes")
    global crawlDeg
    global dbEnd
    crawlDeg.value = 0
    time.sleep(10)
    dbEnd.value = 1
    time.sleep(2)
         

def degreeMonitor(degreeCrawl, degreeVal, dataQ):
    f = open('database/queueLen', 'w')
    secLast = 0
    last = 0
    curr = 0
    flag = False
    while(True):
        #push back by one
        secLast, last, curr = last, curr, dataQ.qsize()
        time.sleep(5)
        f.write("[DEBUG] Queue length = " + str(curr) + ", at time = "+str(time.now())+"\n")
        if(((curr - last) > 1000) and ((last - secLast) > 1000)):
            if flag:
                degreeCrawl.value = degreeCrawl.value - 1
                flag = False
            else:
                flag = True
    

#finds more users, adds user, post, and note info
def userize(userDeck, usersSeen, dataQ, num, end, debug):
    done = 0
    while(done < 360):        
        if end.value:
            return
        if(userDeck):
            done = 0
            result = crawlUser(userDeck, usersSeen, dataQ, num, end, debug)
        else: 
            done += 1
            time.sleep(1)
    return

#wraps a call to dbQ.  Stub functionality for now.
def dataEntry(dataDeck, end, debug):
    done = 0
    while(done < 360):
        if end.value:
            return
        if dbQ:
            done = 0
            dbQ(dataDeck, end, debug)
        else:
            done += 5
            time.sleep(5)
    return

def f1():
    #degree of multiprocessing
    degreeDB = 1
    degreeCrawl=5
    
    global manager
    global crawlDeg
    userDeck = manager.Queue()
    databaseQ = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    crawlDeg.value = degreeCrawl - 1

    ls = []
    for i in range(0, degreeCrawl):
        ls.append(multiprocessing.Process(target=userize, args=(userDeck, usersSeen, databaseQ, i, crawlDeg, True)))
        ls[i].start()
    for j in range(degreeCrawl, (degreeDB+degreeCrawl)):
        ls.append(multiprocessing.Process(target=dataEntry, args=(databaseQ, dbEnd, True)))
        ls[j].start() 
    #end gracefully
    signal.signal(signal.SIGTERM, signal_term_handler)
    for proc in ls:
        proc.join()
    return

def main():
    f1()

if __name__ == '__main__':
    main()
