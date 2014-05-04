#!/usr/bin/python3
import sys
import subprocess
import os
import signal

validInput = ['start', 'stop']
if(len(sys.argv) != 2 or not sys.argv[1] in validInput ):
    print('''Invalid input, valid inputs are:
              start - begin crawl and db processes
              stop - signal crawl and db processes to end ''')
else:
    if sys.argv[1] == 'start':
        if os.path.isfile('crawl.lock'):
            print('A crawler instance is already running\nIf you suspect this is not the case, delete crawl.lock')
        else:
            print("Starting a crawler")
            f = open('crawl.lock', 'w+')
            f.write(str(subprocess.Popen(['python3', 'crawlblr/main.py']).pid))
    else:
        if os.path.isfile('crawl.lock'):
            print("Sending kill message to current crawler instance")
            f = open('crawl.lock', 'r')
            pid = f.readline()
            f.close()
            os.unlink('crawl.lock')
            subprocess.call(['kill', pid])
        else:
            print("There doesn't appear to be a crawler running\nIf you suspect this is not the case, god help you")


