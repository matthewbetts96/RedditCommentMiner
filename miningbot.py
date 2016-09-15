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
unParsedComment = []
committedComments = []
 
print("Starting up Database")
sql = sqlite3.connect('reddit_comments.db')
cur = sql.cursor()
print("Creating database if it doesn't exist")
cur.execute('CREATE TABLE IF NOT EXISTS posts (COMMENTS varchar NOT NULL)')
sql.commit
 
print("Accessing account...")
r = praw.Reddit(app_ua)
r.set_oauth_app_info(app_id, app_secret, app_uri)
r.refresh_access_information(app_refresh)
print('Logged in.')

while (True):
    print("Fetching subreddit " + SUBREDDIT)
    #subreddit = r.get_subreddit(SUBREDDIT)
    print("Fetching Comments...")
    #all_comments = subreddit.get_comments()
    print("Adding comments...")
    for comment in praw.helpers.comment_stream(r, SUBREDDIT):
        text = comment.body
        unParsedComment.append(text)
        joinedComments = ''.join(map(str, unParsedComment))
        if(text in committedComments) == False:
            cur.execute('INSERT INTO posts VALUES (?)', (joinedComments,))
            committedComments.append(joinedComments)
            del unParsedComment[:]	
            sql.commit() 
        del unParsedComment[:]
    print('Pulling new comments')
    del unParsedComment[:]	
    time.sleep(10)
	
	
 
	
		
		

	