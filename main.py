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
crawlEnd = manager.Value('i', 0)

def signal_term_handler(signal, frame):
    print("Terminating child processes")
    global crawlEnd
    global dbEnd
    crawlEnd.value = 1
    time.sleep(10)
    dbEnd.value = 1
    time.sleep(2)
         

def degreeMonitor(dataQ, dbEnd, debug):
    f = open('database/queueLen', 'w')
    f.write("start monitor\n")
    localDeg = 0

    delayStart = 180
    interStitial = 30
    secLast = 0
    last = 0
    curr = 0
    flag = False
    time.sleep(delayStart)
    localWorkers = []
    while(True):
        #push back by one
        secLast, last, curr = last, curr, dataQ.qsize()
        f.write("[DEBUG] Queue length = " + str(curr) + ", changed by " + 
                str(curr - last) + ", at time = "+str(datetime.datetime.today())+"\n")
        f.flush()
        if(((((curr - last) - (last - secLast)) > 5000) or ((curr - last) > 10000)) and (secLast > 50000)): 
            if dbEnd:
                f.write("[DEBUG] end of database situation, killing database spawner")
                return
            if flag:
                for x in range(localDeg, localDeg + 5):
                    localWorkers.append(multiprocessing.Process(target=dataEntry, args=(databaseQ, dbEnd, debug)))
                    localWorkers[x].start()                    
                localDeg += 5
                f.write("[DEBUG] added workers, now at "+str(localDeg)+"\n")
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
        if end.value:
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
    degreeCrawl = 400
    
    global manager
    global crawlEnd
    global dbEnd
    userDeck = manager.Queue()
    databaseQ = manager.Queue()
    userDeck.put('dduane')
    usersSeen = manager.dict()
    usersSeen['dduane'] = 1
    

    ls = []
    for i in range(0, degreeCrawl):
        ls.append(multiprocessing.Process(target=userize, args=(userDeck, usersSeen, databaseQ, crawlEnd, False)))
        ls[i].start()
    for j in range(degreeCrawl, (degDB+degreeCrawl)):
        ls.append(multiprocessing.Process(target=dataEntry, args=(databaseQ, j, dbEnd, False)))
        ls[j].start() 
    #end gracefully
    signal.signal(signal.SIGTERM, signal_term_handler)
    x = multiprocessing.Process(target=degreeMonitor, args=(databaseQ, dbEnd, False))
    x.start()    
    for proc in ls:
        proc.join()
    x.join()
    return

def main():
    f1()

if __name__ == '__main__':
    main()
