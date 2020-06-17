from selenium import webdriver
import json
from celery import Celery
import concurrent.futures

JSON_FILE='tag_url.json'
#app = Celery('tasks', broker='amqp://localhost//')

def scraper(url):
    driver = webdriver.Firefox()
    driver.get(url)
    title = driver.title
    driver.close()
    return

with open(JSON_FILE) as f:
    categories = json.load(f)
    for category_key in categories:
        collection = categories[category_key]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            res = executor.map(scraper(url))
            print(res.result())
        for (category,url) in collection.items():
