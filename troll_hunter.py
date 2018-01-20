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

hot_submissions = subreddit.hot(limit=5)  # number of posts

potential_trolls = []
for submission in hot_submissions:
    # print(dir(submission))
    submission_id = submission.id
    submission = reddit.submission(id=submission_id)

    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        if comment.score <= -10:
            print(comment.author, comment.score, comment.downs) # , comment.body
            if comment.author not in potential_trolls and comment.author != None:
                potential_trolls.append(comment.author)
print(potential_trolls)

for troll in potential_trolls:
    trolls = reddit.redditor(str(troll))
    for comment in trolls.comments.new(limit=None):
        print(comment.author, comment.score, comment.body[:50])
