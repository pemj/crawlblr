from urllib import request, error
import socket
from importer import import_path
import_path('/home/users/pem/crawlblr/beautifulsoup/bs4')
from bs4 import BeautifulSoup
import multiprocessing
import re
import sqlite3
import datetime
from time import sleep
import os
#for some user



def crawlUser(userDeck, usersSeen):
    if hasattr(os, 'getppid'):  # only available on Unix
        pid = os.getppid()
        print('parent process:', pid)
    pid = os.getpid()
    print('process id:', pid)

    conn = sqlite3.connect('/cs/groupprojects/cis632/pem/database/weekday.db')
    c = conn.cursor()
    f = open(('/cs/groupprojects/cis632/pem/database/logfile_'+str(pid)), 'w')
    apikey = "IkJtqSbg6Nd3OBnUdaGl9YWE3ocupygJcnPebHRou8eFbd4RUv"
    blogString = "http://api.tumblr.com/v2/blog/"+username+".tumblr.com/info?api_key="+apikey
    nextPattern = re.compile('.*tumblrReq\.open(\(.*?\))')
    datePattern = re.compile('.*\"date\"\:\"(.*?\")')
    sourcePattern = re.compile('.*source_url\"\:\"http\:\\\\/\\\\/(.*?\.)')
    typePattern = re.compile('.*type\"\:\"(.*?\")')
    postPattern = re.compile('.*\"posts\"\:(.*?,)')
    updatedPattern = re.compile('.*\"updated\"\:(.*?,)')
    notePattern = re.compile('.*\"note_count\"\:(.*?,)')
    fChecker = True
    for i in range(10):
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
        conn.close()
        return "nope"
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
    f.write(str(datetime.datetime.today()))
    while(hasNotes):
        f.write("entering page " + blogURL+(str(pageNum))+"\n")
        f.write(str(datetime.datetime.today()))
        fChecker = True
        for i in range(10):
            try:
                unSouped = request.urlopen(blogURL+(str(pageNum)))
            except error.HTTPError:
                f.write("404: unSouped"+blogURL+str(pageNum)+"\n")
                continue
            except error.URLError:
                f.write("name error, unSoupede:")
            except socket.error:
                f.write("socket error, :")
            else:
                fChecker = False
                break 
        if fChecker:
            conn.commit()
            conn.close()
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
        #f.write("begin post for-loop")
        for post in page.find_all(href=re.compile(noteString)):
            f.write("datetime, post:")
            f.write(str(datetime.datetime.today()))
            #something here is totally amiss.
            hasNotes = True
            #open the notes page for that post
            #f.write("opening post"+ post.get('href')+"\n")
            fChecker = True
            for i in range(10):
                try:
                    notePage = request.urlopen(post.get('href'))
                except error.HTTPError:
                    f.write("404: notePage"+post.get('href')+"\n")
                    continue
                except error.URLError:
                    f.write("name error, unSoupede:")
                except socket.error:
                    f.write("socket error, :")
                else:
                    fChecker = False
                    break 
            if fChecker:
                continue
            preURL = notePage.geturl().split("/post/")
            postNumber = preURL[1].split("/")[0].replace("#notes", "")
            preURL = preURL[0]
            notes = BeautifulSoup(notePage)
            notePage.close()
            uristring = "http://api.tumblr.com/v2/blog/"+username+".tumblr.com/posts?api_key="+apikey+"&id="+postNumber
            fChecker = True
            for i in range(10):
                try:
                    uribject = request.urlopen(uristring)
                except error.HTTPError:
                    f.write("404, uribject: "+uristring+"\n")
                except error.URLError:
                    f.write("name error, unSouped:")
                except socket.error:
                    f.write("socket error, :")
                else:
                    fChecker = False
                    break 
            if fChecker:
                continue
            apiBlob = BeautifulSoup(uribject).prettify()
            uribject.close()
            postDate = re.search(datePattern, apiBlob).groups(1)[0]
            postSource = re.search(sourcePattern, apiBlob)
            noteCount = re.search(notePattern, apiBlob).groups(1)[0].rstrip(",")
            if postSource:
                postSource = postSource.groups(1)[0].rstrip(".")
            else:
                postSource = username
            postType = re.search(typePattern, apiBlob)
            postType = postType.groups(1)[0].rstrip('\"')
            #for each fifty-note page
            while (1):
                f.write("datetime, notepage:")
                f.write(str(datetime.datetime.today())+"\n")
                noteChunk = notes("ol", class_="notes")
                if not noteChunk:
                    #f.write("breaking via noteChunk\n")
                    break
                noteChunk = noteChunk[0]
                #for each note on that page
                theseArgs = []
                for link in noteChunk.find_all('li'):
                    noteType = ""
                    #figure out name of person who's noting
                    identity = link.a.get('href')
                    identity = identity.lstrip("http:").lstrip("/").partition('.')[0]
                    if (identity == "#"):
                        continue
                    if (identity not in usersSeen):
                        userDeck.put(identity)
                        usersSeen[identity] = 1
                    usersSeen[identity] += 1

                    #figure out if this was posted by a follower
                    if (link.a.get('rel')[0] == 'nofollow'):
                        isFollowee = False
                    else:
                        isFollowee = True
                    #figure out what type of note we're dealing with
                    if "reblogged" in link.span.text:
                        noteType = "reblog"
                    if "likes" in link.span.text:
                        noteType = "like"
                    #figure out who they reblogged it from.  If it's a like, emptystring.
                    rebloggedFrom = link.span.find_all('a', class_="source_tumblelog")
                    if not rebloggedFrom:
                        rebloggedFrom = ""
                    else:
                        rebloggedFrom = rebloggedFrom[0].get('href').replace("http://", "").replace(".tumblr.com", "")                       
                    theseArgs.append((identity, rebloggedFrom, postNumber, noteType))
                    f.write("note: "+str(theseArgs) + "\n")
                    #break
                for notepiece in theseArgs:
                    c.execute('INSERT INTO notes (username, rebloggedFrom, postID, type) ' +
                              'VALUES (?,?,?,?);', notepiece)   
                conn.commit()
                nextNotes = notes("li", class_="note more_notes_link_container")
                if (not nextNotes):
                    break
                localText = nextNotes[0].prettify()
                localText = re.search(nextPattern, localText)
                localText = localText.groups(1)[0].split("/")[3].rstrip("\',true)")
                localText = preURL+"/notes/"+postNumber+"/"+localText
                f.write("localText: "+localText+"\n")
                fChecker = True
                for i in range(10):
                    try:
                        localbject = request.urlopen(localText)
                    except error.HTTPError:
                        f.write("404, localText: "+localText+"\n")
                    except error.URLError:
                        f.write("name error, unSoupede:")
                    except socket.error:
                        f.write("socket error, :")
                    else:
                        fChecker = False
                        break 
                if fChecker:
                    break                    
                notes = BeautifulSoup(localbject)
                localbject.close()
                nextNotes = []
            cargs = (username, postSource, postNumber, postType, postDate, noteCount)
            f.write("post written: "+str(cargs))
            c.execute('insert into posts values (?,?,?,?,?, ?)', cargs)   
  
            
            
    c.execute('insert into users values (?,?,?)', 
                      (username, updated, postCount))
    conn.commit()
    conn.close()
    return "yeah"

