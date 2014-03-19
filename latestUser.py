import sqlite3
import pickle
conn = sqlite3.connect('finaltimate.db')
c = conn.cursor()
noteArray = []
for row in c.execute('''SQL HAPPENS HR PLZ'''):
    noteArray.append(row)

lastElement = noteArray[0][0]
likeD = dict()
reblogD = dict()
likeLs = dict()
reblogLs = dict()
for tup in noteArray:
    src, dst, typ = tup
    if lastElement != src:
        likeLs[lastElement] = likeD
        reblogLs.[lastElement] = reblogD
        lastElement = src
        likeD = dict()
        reblogD = dict()

    if typ == "reblog":
        if dst not in reblogD:
            reblogD[dst] = 1
        else:
            reblogD[dst] += 1
    elif typ == "like":
        if dst not in likeD:
            likeD[dst] = 1
        else:
            likeD[dst] += 1    


with open('data.pickle', 'wb') as f:
    # Pickle the dictionaries using the highest protocol available.
    pickle.dump((likeD, reblogD), f, pickle.HIGHEST_PROTOCOL)


reblogged = set()
for k, v in reblogD.items():
    for k2, v2 in v.items():
        reblogged.add((k, k2, v2))

liked = set()
for k, v in likeD.items():
    for k2, v2 in v.items():
        if v2 > 3:
            liked.add((k, k2, v2))
total = set.intersection(liked, reblogged)
f = open('userRelations.txt', 'w')
for item in total:
    f.write(str(item)+"\n")

    
