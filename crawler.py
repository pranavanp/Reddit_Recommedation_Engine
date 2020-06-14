import praw
import json
import yake

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

url = "https://www.reddit.com/r/uwaterloo/comments/gomj1g/how_to_get_good_algorithms_and_data_structures/"
submission = reddit.submission(url=url)
print(submission.selftext)

submission.comments.replace_more(limit=None)
for comment in submission.comments.list():
    print(comment.body)

print(submission.comments.list())