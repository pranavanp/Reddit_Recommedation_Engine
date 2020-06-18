import nltk
import praw
import json
from Cleaner import Cleaner
import yake

class SearchGenerator:
    def __init__(self, url):
        self.url = url

    def create_reddit(self, json_file="reddit_config.json", json_key="reddit_user_values"):
        with open(json_file) as f:
            data = json.load(f)
            user_values = data[json_key]
            reddit = praw.Reddit(client_secret=user_values['client_secret'],
                                 client_id=user_values['client_id'],
                                 user_agent=user_values['user_agent'],
                                 username=user_values['username'],
                                 password=user_values['password'])
            return reddit

    def get_title(self):
        return self.submission.title

    def get_body(self):
        return self.submission.selftext

    def get_subreddit(self):
        self.subreddit = self.submission.subreddit

    def get_comments(self):
        text = ""
        self.submission.comments.replace_more(limit=None)
        for comment in self.submission.comments.list():
            text += ' ' + comment.body
        return text

    def scrape_submission(self):
        reddit = self.create_reddit()
        self.submission = reddit.submission(url=url)
        text = self.get_title()
        text += ' ' + self.get_body()
        if len(text) <= 1000:
            text += ' ' + self.get_comments()
        return text

    def get_cleantext(self, text):
        cleaner = Cleaner()
        cleaned = cleaner.clean_text(text)
        return cleaned

    def extract_keywords(self):
        content= self.get_cleantext(self.scrape_submission())
        simple_kwextractor = yake.KeywordExtractor(content)
        keywords = simple_kwextractor.extract_keywords(n=1)
        return keywords

url = "https://www.reddit.com/r/uwaterloo/comments/gomj1g/how_to_get_good_algorithms_and_data_structures/"
run=SearchGenerator(url)
print(run.extract_keywords())
