import pandas as pd

df = pd.read_csv('results.csv')
print(df.to_string())

from Cleaner import Cleaner
from ThreadScraper import ThreadScraper

class Content:

    def __init__(self, db_file):
        self.df = pd.read_csv('results.csv')
        self.cleaner = Cleaner()

    def __iter__(self):
        for id in self.get_ids():
            page = self.get_page_by_id(id)
            yield self.cleaner.clean_text(page).split()