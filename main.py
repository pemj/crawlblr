# /usr/bin/python3
import datetime
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
    global crawlEnd
    global degreeDB
    crawlEnd.value = 1
    time.sleep(10)
    dbEnd.value = 1x
    time.sleep(2)
         

def degreeMonitor(dataQ):
    f = open('database/queueLen', 'w')
    f.write("start monitor\n")
    global degreeDB

    delayStart = 180
    interStitial = 25
    secLast = 0
    last = 0
    curr = 0
    flag = False
    time.sleep(delayStart)
    while(True):
        #push back by one
        secLast, last, curr = last, curr, dataQ.qsize()
        f.write("[DEBUG] Queue length = " + str(curr) + ", at time = "+str(datetime.datetime.today())+"\n")
        f.flush()
        if(((((curr - last) - (last - secLast)) > 5000) or ((curr - last) > 10000)) and (secLast > 50000)):
            if degreeDB.value == 0:
                return                
            if flag:
                degreeDB.value = degreeDB.value + 3
                f.write("[DEBUG] added work, now at "+str(degreeDB.value)+"\n")
                flag = False
            else:
                flag = True
        else:
            flag = False
        time.sleep(interStitial)

#finds more users, adds user, post, and note info
def userize(userDeck, usersSeen, dataQ, end, debug):
    done = 0
    while(done < 360):        
        if end.value < num:
            return
        if(userDeck):
            done = 0
            result = crawlUser(userDeck, usersSeen, dataQ, end, debug)
        else: 
            done += 1
            time.sleep(1)
    return

#wraps a call to dbQ.  Stub functionality for now.
def dataEntry(dataDeck, num, end, debug):
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
    degDB = 200
    degreeCrawl = 600
    
    global manager
    global crawlEnd
    userDeck = manager.Queue()
    databaseQ = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    

    ls = []
    x = multiprocessing.Process(target=degreeMonitor, args=(databaseQ,))
    x.start()
    for i in range(0, degreeCrawl):
        ls.append(multiprocessing.Process(target=userize, args=(userDeck, usersSeen, databaseQ, crawlEnd, False)))
        ls[i].start()
    for j in range(degreeCrawl, (degDB+degreeCrawl)):
        ls.append(multiprocessing.Process(target=dataEntry, args=(databaseQ, j, dbEnd, False)))
        ls[j].start() 
    #end gracefully
    signal.signal(signal.SIGTERM, signal_term_handler)
    for proc in ls:
        proc.join()
    x.join()
    return

def main():
    f1()

if __name__ == '__main__':
    main()
