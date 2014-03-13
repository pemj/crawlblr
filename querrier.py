import sqlite3
#get most popular types of posts
postPopularity = '''SELECT type, count(type) + noteCount AS count
FROM posts
GROUP BY postType
ORDER BY count'''


#get number of posts and reblogs from users
reblogPostPopularity = '''SELECT DISTINCT op.username, reblogs.count, original.count + reblogs.count AS total
FROM posts op
INNER JOIN 
	(SELECT username, count(username) AS count 
	 FROM notes 
	 WHERE type = "reblog" 
	 GROUP BY username) reblogs 
ON op.username  = reblogs.username
INNER JOIN 
	(SELECT username, count(username) AS count 
	 FROM posts 
	 GROUP BY username) original 
ON op.username = original.username'''


#Get user relations, likes and reblogs
userRelations = '''SELECT DISTINCT original.username AS source, reblogs.count AS reblogs, likes.count AS likes, likes.destination AS recipient, reblogs.destination AS filter
FROM notes original
INNER JOIN 
	(SELECT DISTINCT notes.username AS source, COUNT(*) AS count, posts.username AS destination 
	 FROM notes 
	 INNER JOIN posts 
	 ON notes.postID = posts.postID 
	 WHERE notes.type="reblog" 
	 GROUP BY source, destination) reblogs
ON original.username = reblogs.source
INNER JOIN
	(SELECT DISTINCT notes.username AS source, count(*) AS count, posts.username AS destination 
	 FROM notes 
	 INNER JOIN posts 
	 ON notes.postID = posts.postID 
	 WHERE notes.type="like" 
	 GROUP BY source, destination) likes
ON original.username = likes.source
WHERE filter = recipient AND likes.count >= 3'''



conn = sqlite3.connect('finaltimate.db')
c = conn.cursor()

f = open('popularity.txt', 'w')
for row in c.execute(postPopularity):
    f.write(row)
f.close()

f = open('reblogsvsoriginal.txt', 'w')
for row in c.execute(reblogPostPopularity):
    f.write(row)
f.close()

f = open('userRelations.txt', 'w')
for row in c.execute(userRelations.txt):
    f.write(row)
f.close()
