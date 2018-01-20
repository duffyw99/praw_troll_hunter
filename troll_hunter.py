import praw
import re
from admin_ignore.praw_keys import * # clint_id, client_secret, pw, etc.
import random
import time

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password,
                     )

subreddit = reddit.subreddit('all')

hot_submissions = subreddit.hot(limit=1)  # number of posts

# Find comments with scores below zero to identify potential troll users
for submission in hot_submissions:
    # print(dir(submission))
    submission_id = submission.id
    submission = reddit.submission(id=submission_id)

    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        if comment.score < 0:
            print(comment.author, comment.body, comment.score, comment.downs)
