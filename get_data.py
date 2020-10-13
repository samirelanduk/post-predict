import praw
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

for subreddit in SUBREDDITS:
    print(list(reddit.subreddit(subreddit).new(limit=5)))

"""
Every 30 seconds, get a random new text post from one the subreddits, with:
id
time
title
content
subreddit
subreddit stats at time

After one week this will be ~20000 entries

# Then a week later go back and get how many comments and karma it got
"""

    