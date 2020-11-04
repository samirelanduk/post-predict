import praw
import time
from itertools import cycle
import random
import sqlite3
from secrets import REDDIT_USERNAME, REDDIT_PASSWORD
from secrets import REDDIT_CLIENT_ID, REDDIT_SECRET

reddit = praw.Reddit(
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="Post Predict",
)

SUBREDDITS = [
    "askreddit",
    "NoStupidQuestions",
    "tifu",
    "relationship_advice",
    "legaladvice"
]


conn = sqlite3.connect("data.db")
c = conn.cursor()

c.execute('''CREATE TABLE posts
             (id, timestamp, subreddit, title, is_self, text, subscribers,
              active_users, comments_at_start, score_at_start, comments_hour,
              score_hour, comments_day, score_day, comments_week, score_week)''')
conn.commit()

for subreddit_name in cycle(SUBREDDITS):
    subreddit = reddit.subreddit(subreddit_name)
    posts = list(subreddit.new(limit=20))

    # Get new posts
    for post in posts:
        c.execute("SELECT * FROM posts WHERE id=?", [post.id])
        row = c.fetchone()
        if not row:
            c.execute("INSERT INTO posts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [
                post.id, post.created_utc, subreddit_name, post.title,
                post.is_self, post.selftext, subreddit.subscribers,
                int(subreddit.active_user_count), int(post.num_comments), post.score,
                None, None, None, None, None, None
            ])
            conn.commit()

    # Update old posts
    hour_ago = time.time() - 3600
    to_update = c.execute("SELECT * FROM posts WHERE timestamp < ? AND comments_hour ISNULL", [hour_ago]) 
    for row in to_update.fetchall():
        post = reddit.submission(id=row[0])
        c.execute("UPDATE posts SET comments_hour = ?, score_hour = ? WHERE id = ?", [
            post.num_comments, post.score, row[0]
        ])
        conn.commit()
    
    day_ago = time.time() - 86400
    to_update = c.execute("SELECT * FROM posts WHERE timestamp < ? AND comments_day ISNULL", [day_ago]) 
    for row in to_update.fetchall():
        post = reddit.submission(id=row[0])
        c.execute("UPDATE posts SET comments_day = ?, score_day = ? WHERE id = ?", [
            post.num_comments, post.score, row[0]
        ])
        conn.commit()
    
    week_ago = time.time() - (86400 * 7)
    to_update = c.execute("SELECT * FROM posts WHERE timestamp < ? AND comments_week ISNULL", [week_ago]) 
    for row in to_update.fetchall():
        post = reddit.submission(id=row[0])
        c.execute("UPDATE posts SET comments_week = ?, score_week = ? WHERE id = ?", [
            post.num_comments, post.score, row[0]
        ])
        conn.commit()


    time.sleep(5)


conn.close()

    