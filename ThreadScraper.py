import pandas as pd
import json
from SearchGenerator import SearchGenerator
import concurrent.futures
import openpyxl
import time
import apraw
import praw
import asyncio
import aiohttp
import numpy as np
from numba import njit,jit


start_time = time.time()

res_dict={'Title':[],
          'Content':[],
          'URL':[],
          'ID':[]}

url = "https://www.reddit.com/r/uwaterloo/comments/gomj1g/how_to_get_good_algorithms_and_data_structures/"
sg=SearchGenerator(url)
search_terms=sg.extract_keywords()
search_terms = np.asarray(search_terms)
@jit(nogil=True)
def get_submissions(term):
    global res_dict
    submissions = (sg.get_reddit().subreddit(str(sg.get_subreddit()))).search(term[0],time_filter='year',syntax='plain')
    for sub in submissions:
        title = sub.title
        content = sub.selftext
        url = sub.url
        id = sub.id
        if not (url.endswith(".jpg")) and not (url.endswith(".png")) and not (url.endswith(".gif")) and len(
                content) > 50 and ('http' not in content) and (id not in res_dict['ID']):
            res_dict['Title'].append(title)
            res_dict['Content'].append(content)
            res_dict['URL'].append(url)
            res_dict['ID'].append(id)


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(8) as executor:
        executor.map(get_submissions,search_terms)
    df = pd.DataFrame(res_dict)
    df.dropna(inplace=True)
    df.reset_index()
    print("Writing to CSV")
    df.to_csv('results.csv')
    print("Done...")
    print(df.to_string())
    print(time.time() - start_time)