import sqlite3
import pickle
conn = sqlite3.connect('finaltimate.db')
c = conn.cursor()
noteArray = []
#for likes
for row in c.execute('''SELECT notes.username AS source,  posts.username AS destination
FROM notes
INNER JOIN posts
ON notes.postID = posts.postID
WHERE notes.type = "like"
ORDER BY notes.username'''):
    likeArray.append(row)

#for reblogs
for row in c.execute('''SELECT username AS source, rebloggedFrom AS destination
FROM notes
WHERE notes.type = "reblog"
ORDER BY username'''):
    reArray.append(row)

likeD = dict()
reblogD = dict()
likeLs = dict()
reblogLs = dict()

lastElement =likeArray[0][0]
for note in likeArray:
    src, dst = note
    if lastElement != src:
        likeLs[lastElement] = likeD
        lastElement = src
        likeD = dict()        
    if dst not in likeD:
        likeD[dst] = 1
    else:
        likeD[dst] += 1

lastElement = reArray[0][0]
for note in reArray:
    src, dst = note
    if lastElement != src:
        reblogLs[lastElement] = reblogD
        lastElement = src
        reblogD = dict()        
    if dst not in reblogD:
        reblogD[dst] = 1
    else:
        reblogD[dst] += 1    

with open('data.pickle', 'wb') as f:
    # Pickle the dictionaries using the highest protocol available.
    pickle.dump((likeD, reblogD), f, pickle.HIGHEST_PROTOCOL)


reblogged = set()
for k, v in reblogLs.items():
    for k2, v2 in v.items():
        reblogged.add((k, k2, v2))

liked = set()
for k, v in likeLs.items():
    for k2, v2 in v.items():
        if v2 > 2:
            liked.add((k, k2, v2))

total = set.intersection(liked, reblogged)
f = open('userRelations.txt', 'w')
for item in total:
    f.write(str(item)+"\n")   
