from urllib import request, error
import socket
from bs4 import BeautifulSoup
from multiprocessing import Queue, Manager
from queue import Empty
import re
import datetime
from time import sleep
import os
#for some user


#opens a URL, uses JSON decoding to turn it into a dictionary, checks 
#for validity.  Retries a few times if it breaks
#Parameters: 
#url: type: string, contents: URL representing a tumblr API request
#segment: type: string, contents: the code segment identifier
def openSafely(url, segment):
    fChecker = True
    for i in range(2):
        try:
            page = request.urlopen(url)
        except error.HTTPError:
            f.write("404, "+segment+": "+url+"\n")
            break
        except error.URLError:
            f.write("URL error, "+segment+"\n")
            break
        except socket.error:
            f.write("socket error, "+segment+"\n")
            break
        else:
            fChecker = False
            break 
    if fChecker:
        f.write("unknown error in "+segment+"\n")
        return False

    page = page.read().decode('utf-8')
    if(info['meta']['msg'] != "OK"):
        f.write("Bad " + segment + " page, error code" + info['meta']['msg'])
        return "nope"
    return page




def crawlUser(userDeck, usersSeen, dataQ, end, debug):
    try:
        username = userDeck.get(True, 5)
    except Empty:
        return "nope\n"           
    if hasattr(os, 'getppid'):  # only available on Unix
        pid = os.getppid()
        print('parent process:', pid)
    pid = os.getpid()
    print('process id:', pid)
    f = open(('database/crawlers/logfile_'+str(pid)), 'w')
    f.write("begin crawler"+ str(pid)+"\n")
    
    apikey = "IkJtqSbg6Nd3OBnUdaGl9YWE3ocupygJcnPebHRou8eFbd4RUv"
    blogString = "http://api.tumblr.com/v2/blog/"+username+".tumblr.com/info?api_key="+apikey
    postString = "http://api.tumblr.com/v2/blog/"+username+".tumblr.com/posts?api_key="+apikey
    noteString = "http://api.tumblr.com/v2/blog/"+username+".tumblr.com/likes?api_key="+apikey


    ##################################USER section######################
    #get user info
    info = openSafely(blogString, "user info")
    if not info:
        return "info error"

    blogURL = info['response']['blog']['url']
    username = info['response']['blog']['title']
    updated = info['response']['blog']['updated']
    #how stupid is that line up there, right?  Just, just let it go.
    postCount = info['response']['blog']['posts']
    #if they make likes public
    if info['response']['blog']['share_likes']:
        likeCount = info['response']['blog']['likes']
    else:
        likeCount = -1
    userArgs = (username, updated, postCount, likeCount)
    if debug:
        f.write("[DEBUG] user written: "+str(userArgs) + "\n")
    #off to the database
    dataQ.put(userArgs)
    
    
    #################################POSTS section######################
    
    offset=0
    previousPosts = set()
    recentPosts = set()
    #while we have yet to hit the final posts
    while(offset < postCount):

        if(debug):
            f.write("[DEBUG] user:" + username+", post offset: "+(str(offset))+"\n")
            #try to open the post page
        posts = openSafely(poststring+"&notes_info=True&reblog_info&offset="+(str(offset)))
        if not posts:
            continue


        #for each post in our returned post object
        for post in posts['response']['posts']:
            postNumber = post['id']
            if postNumber in previousPosts:
                continue
            recentPosts.push(postNumber)
            
            postType = post['type']
            postDate = post['timestamp']
            noteCount = post['note_count']
#########Reblogged Section###################
            if 'reblogged_from_name' in post.keys():
                identity = post['reblogged_from_name']
                noteArgs = (username, identity, postNumber, "reblog")
                dataQ.put(noteArgs)
                if (identity not in usersSeen):
                    usersSeen[identity] = 0
                    userDeck.put(identity)
                usersSeen[identity] += 1
                continue

            postArgs = (username, postNumber, postType, postDate, noteCount)
            if debug:
                f.write("[DEBUG] post written: "+str(postArgs) + "\n")
            dataQ.put(postArgs)
        previousPosts = recentPosts
        recentPosts = set()

    #################################LIKES section######################
    offset=0
    #while we have yet to hit the final likes
    while(offset < likeCount):
        if(debug):
            f.write("[DEBUG] user:" + username+", note offset: "+(str(offset))+"\n")
            #try to open the note page
        notes = openSafely(notestring+(str(offset)))
        if not notes:
            continue

        #for each post in our returned post object
        for note in notes['response']['liked_posts']:
            postNumber = note['id']
            noteType = "like"
            rebloggedFrom = note['blog_name']
            noteArgs = (username, rebloggedFrom, postNumber, noteType)
            if debug:
                f.write("[DEBUG] like written: "+str(noteArgs) + "\n")
            dataQ.put(noteArgs)
            note['id']
