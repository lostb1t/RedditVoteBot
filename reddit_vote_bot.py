#!/usr/bin/env python3

import praw
import os
import threading
from dotenv import load_dotenv

load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("PRAW_CLIENT_ID"),
    client_secret=os.environ.get("PRAW_CLIENT_SECRET"),
    user_agent=os.environ.get("PRAW_USER_AGENT"),
    username=os.environ.get("PRAW_USERNAME"),
    password=os.environ.get("PRAW_PASSWORD")
)

def vote_on_comments(user, vote_type, limit):
    print('Beginning to {} user {}. The permalink to the comment will be printed when a comment is downvoted.', vote_type, user)
    for comment in user.comments.new(limit=limit):
        if vote_type == 'upvote':
            comment.upvote()
        elif vote_type == 'downvote':
            comment.downvote()
        #already_done.add(comment.id)
        print(comment.permalink)

def run_bot():
    limit=os.environ.get("LIMIT", 500)
    vote_type=os.environ.get("VOTE_TYPE", "downvote")
    users=os.environ.get("TARGET_USER")
    users = users.split(",")

    #while True:
    for username in users:
        user = reddit.redditor(username)
        t = threading.Thread(target=vote_on_comments, args=(user, vote_type, limit))
        t.start()


if __name__ == '__main__':
    print("starting")
    run_bot()