import praw
from admin_ignore.praw_keys import *  # clint_id, client_secret, pw, etc.
import json
import re
import random
import time

# Establish connection to reddit
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password,
                     )

karma_threshold = -10
subreddit = reddit.subreddit('all')
hot_submissions = subreddit.hot(limit=5)  # number of posts

# Load known trolls
with open('troll_registry.txt', 'r') as f:
    potential_trolls = [line.strip() for line in f]

# Scan comments from top posts for negitive comments
for submission in hot_submissions:
    # print(dir(submission))
    submission_id = submission.id
    submission = reddit.submission(id=submission_id)

    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        if comment.score <= karma_threshold:
            print(comment.author, comment.score, comment.downs)  # ,comment.body
            if comment.author not in potential_trolls and comment.author is not None:
                potential_trolls.append(comment.author)

with open('troll_registry.txt', 'w') as file:
    for troll in potential_trolls:
        file.write("%s\n" % troll)
        trolls = reddit.redditor(str(troll))
        for comment in trolls.comments.new(limit=None):
            if comment.score < karma_threshold:
                print(comment.author,
                      comment.subreddit,
                      comment.score,
                      comment.body[:50])
