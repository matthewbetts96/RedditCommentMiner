app_ua = 'Comment collector by uMatthewBetts'
app_id = ''
app_secret = ''
app_uri = 'https://127.0.0.1:65010/authorize_callback'
app_scopes = 'account creddits edit flair history identity livemanage modconfig modcontributors modflair modlog modothers modposts modself modwiki mysubreddits privatemessages read report save submit subscribe vote wikiedit wikiread'
app_refresh = ''

import praw
import time
import sqlite3

SUBREDDIT =  'all'

print("Starting up Database")
sql = sqlite3.connect('reddit_comments.db')
cur = sql.cursor()
print("Creating database if it doesn't exist")
cur.execute('CREATE TABLE IF NOT EXISTS posts (BODY varchar NOT NULL, AUTHOR varchar NOT NULL, SUBREDDIT varchar NOT NULL, SUBREDDIT_ID varchar NOT NULL)')
sql.commit()

print("Accessing account...")
r = praw.Reddit(app_ua)
r.set_oauth_app_info(app_id, app_secret, app_uri)
r.refresh_access_information(app_refresh)
print('Logged in.')

while (True):
	try:
		print("Fetching subreddit " + SUBREDDIT)
		print("Fetching Comments...")
		print("Adding comments...")
		for comment in praw.helpers.comment_stream(r, SUBREDDIT):			
			commentbody = comment.body
			commentAuthor = comment.author
			commentSubreddit = comment.subreddit
			commentSubredditID = comment.subreddit_id
			cur.execute('INSERT INTO posts(BODY, AUTHOR, SUBREDDIT, SUBREDDIT_ID) VALUES (?,?,?,?)',(str(commentbody),str(commentAuthor),str(commentSubreddit),str(commentSubredditID),))
			sql.commit()
	except :
		print("An error occured, skipping this comment...")
		

	
