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



def crawlUser(userDeck, usersSeen, dataQ, num, end, debug):
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
    #compile some regular expressions for rapid searches later
    nextPattern = re.compile('.*tumblrReq\.open(\(.*?\))')
    datePattern = re.compile('.*\"date\"\:\"(.*?\")')
    sourcePattern = re.compile('.*source_url\"\:\"http\:\\\\/\\\\/(.*?\.tumblr\.com)')
    typePattern = re.compile('.*type\"\:\"(.*?\")')
    postPattern = re.compile('.*\"posts\"\:(.*?,)')
    updatedPattern = re.compile('.*\"updated\"\:(.*?,)')
    notePattern = re.compile('.*\"note_count\"\:(.*?,)')
    prevPost = set()
    
    #Open first user page
    fChecker = True
    for i in range(5):
        try:
            blogject = request.urlopen(blogString)
        except error.HTTPError:
            f.write("404, invalid username: "+blogString+"\n")
            break
        except error.URLError:
            f.write("name error, username:")
            break
        except socket.error:
            f.write("socket error, blogject:")
            break
        else:
            fChecker = False
            break 
    if fChecker:
        f.write("unknown error in blogString\n")
        return "nope"
        
    #parse user page
    infoBlob = BeautifulSoup(blogject).prettify()
    blogject.close()
    postCount = re.search(postPattern, infoBlob)
    postCount = postCount.groups(1)[0].rstrip(",")
    updated = re.search(updatedPattern, infoBlob)
    updated = updated.groups(1)[0].rstrip(",")

    #we'll want to grab the name and post-count from user.
    
    #Then we want to grab the post ID for each of their posts.
    
    # then, 
    
    #initialize some conditions.
    hasNotes = True
    blogURL = "http://"+username+".tumblr.com/page/"
    pageNum = 0

    #while our page has posts on it
    while(hasNotes):
        if(debug):
            f.write("[DEBUG] page:" + blogURL+(str(pageNum))+"\n")
        #try to open the post page
        fChecker = True
        for i in range(5):
            try:
                unSouped = request.urlopen(blogURL+(str(pageNum)))
            except error.HTTPError:
                f.write("[ERROR] 404: unSouped"+blogURL+str(pageNum)+"\n")
                continue
            except error.URLError:
                f.write("[ERROR] name error: unSouped\n")
            except socket.error:
                f.write("[ERROR] socket error: unSouped\n")
            else:
                fChecker = False
                break 
        if fChecker:
            return "nope"

        pageNum += 1
        #store this for when we have to extract note strings from a page
        pageName = unSouped.geturl()
        noteString, nil, nil = pageName.rpartition("/page/")
        noteString = noteString + "/post/"

        page = BeautifulSoup(unSouped)        
        unSouped.close()
        hasNotes = False
        #for each post in a page     
        for post in page.find_all(href=re.compile(noteString)):              
            hasNotes = True
            if debug:
                f.write("[DEBUG] opening post: "+ post.get('href')+"\n")
            #open the notes page for that post
            fChecker = True
            for i in range(5):
                try:
                    notePage = request.urlopen(post.get('href'))
                except error.HTTPError:
                    f.write("[ERROR] 404: notePage "+post.get('href')+"\n")
                    continue
                except error.URLError:
                    f.write("[ERROR] name error: notePage\n")
                except socket.error:
                    f.write("[ERROR] socket error: notePage\n")
                else:
                    fChecker = False
                    break 
            if fChecker:
                continue
            #woo erorr checking
            check = post.get('href')
            if check.find("http://www.facebook.com/") != -1:
                continue
            preURL = notePage.geturl().split("/post/")
            try:
                postNumber = preURL[1].split("/")[0].replace("#notes", "")
            except IndexError:
                continue
            preURL = preURL[0]
            notes = BeautifulSoup(notePage)
            notePage.close()
            uristring = "http://api.tumblr.com/v2/blog/"+username+".tumblr.com/posts?api_key="+apikey+"&id="+postNumber

            #open an api page to get some post metadata
            fChecker = True
            for i in range(5):
                try:
                    uribject = request.urlopen(uristring)
                except error.HTTPError:
                    f.write("[ERROR] 404, uribject: "+uristring+"\n")
                except error.URLError:
                    f.write("[ERROR] name error: uribject")
                except socket.error:
                    f.write("[ERROR] socket error: uribject")
                else:
                    fChecker = False
                    break 
            if fChecker:
                continue

            apiBlob = BeautifulSoup(uribject).prettify()
            uribject.close()
            try:
                postDate = re.search(datePattern, apiBlob).groups(1)[0]
                postSource = re.search(sourcePattern, apiBlob)
                noteCount = re.search(notePattern, apiBlob).groups(1)[0].rstrip(",")
            except AttributeError:
                continue
            if postSource:
                postSource = postSource.groups(1)[0].rstrip(".")
                if(postSource in usersSeen):
                    continue
                usersSeen[postSource] = 1
                userDeck.put(postSource)
                continue
            else:
                postSource = username

            if postNumber in prevPost:
                continue
            prevPost.add(postNumber)
            postType = re.search(typePattern, apiBlob)
            postType = postType.groups(1)[0].rstrip('\"')
            #for each fifty-note page
            while (1):
                if debug:
                    f.write("[DEBUG]: notepage\n")
                noteChunk = notes("ol", class_="notes")
                if not noteChunk:
                    if debug:
                        f.write("[DEBUG] breaking via noteChunk\n")
                    break
                noteChunk = noteChunk[0]
                #for each note on that page
                theseArgs = []
                for link in noteChunk.find_all('li'):
                    noteType = ""
                    #figure out name of person who's noting
                    try:
                        identity = link.a.get('href')
                    except AttributeError:
                        continue
                    identity = identity.lstrip("http:").lstrip("/").partition('.')[0]
                    if (identity == "#"):
                        continue
                    if (identity not in usersSeen):
                        usersSeen[identity] = 1
                        userDeck.put(identity)
                    usersSeen[identity] += 1

                    #figure out if this was posted by a follower
                    if (link.a.get('rel')[0] == 'nofollow'):
                        isFollowee = False
                    else:
                        isFollowee = True
                    #figure out what type of note we're dealing with
                    try:
                        if "reblogged" in link.span.text:
                            noteType = "reblog"
                    except AttributeError:
                        continue
                    if "likes" in link.span.text:
                        noteType = "like"
                    #figure out who they reblogged it from.  If it's a like, emptystring.
                    rebloggedFrom = link.span.find_all('a', class_="source_tumblelog")
                    if not rebloggedFrom:
                        rebloggedFrom = ""
                    else:
                        rebloggedFrom = rebloggedFrom[0].get('href').replace("http://", "").replace(".tumblr.com/", "")                       
                    dataQ.put((identity, rebloggedFrom, postNumber, noteType))
                    if end.value < num:
                        dataQ.put((username, updated, postCount))
                        f.write("[EXIT] received exit, shutting down process " + str(pid)+"\n")
                        return "yeah"

                nextNotes = notes("li", class_="note more_notes_link_container")
                if (not nextNotes):
                    break
                localText = nextNotes[0].prettify()
                localText = re.search(nextPattern, localText)
                localText = localText.groups(1)[0].split("/")[3].rstrip("\',true)")
                localText = preURL+"/notes/"+postNumber+"/"+localText
                fChecker = True
                for i in range(5):
                    try:
                        localbject = request.urlopen(localText)
                    except error.HTTPError:
                        f.write("[ERROR] 404: localText: "+localText+"\n")
                    except error.URLError:
                        f.write("[ERROR] name error: localbject")
                    except socket.error:
                        f.write("[ERROR] socket error: localbject")
                    else:
                        fChecker = False
                        break 
                if fChecker:
                    break                    
                notes = BeautifulSoup(localbject)
                localbject.close()
                nextNotes = []
            cargs = (username, postNumber, postType, postDate, noteCount)
            if debug:
                f.write("[DEBUG] post written: "+str(cargs) + "\n")
            dataQ.put(cargs)
           
    if debug:
        f.write("[DEBUG] user written: " + username + "\n")
    dataQ.put((username, updated, postCount))        
    return "yeah"

