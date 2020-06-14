import praw
import json
import pandas as pd

def create_reddit_object(json_file="reddit_config.json",json_key="reddit_user_values"):
    with open(json_file) as f:
        data = json.load(f)
        user_values=data[json_key]
        reddit = praw.Reddit(client_id=user_values['client_id'],
                             client_secret=user_values['client_secret'],
                             user_agent=user_values['user_agent'],
                             username=user_values['username'],
                             password=user_values['password'])
        return reddit

reddit=create_reddit_object()

subred=reddit.subreddit("learnprogramming")
hot=subred.hot(limit=11)
for i in hot:
    print(i.title,i.url)
