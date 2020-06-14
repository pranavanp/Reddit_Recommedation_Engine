import requests
import csv
import time
from bs4 import BeautifulSoup

url = "https://old.reddit.com/r/datascience/"
# Headers to mimic a browser visit
headers = {'User-Agent': 'Mozilla/5.0'}

# Returns a requests.models.Response object
page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')
domains = soup.find_all("span", class_="domain")

for domain in domains:
    if domain != "(self.datascience)":
        continue

    print(domain.text)