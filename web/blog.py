import urllib.request
from newspaper import Article
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
import sys

searchQuery = sys.argv[1]

BASE_URL = "https://search.naver.com/search.naver?where=post&sm=tab_jum&ie=utf8&query="+quote(searchQuery)
soup = BeautifulSoup(urllib.request.urlopen(BASE_URL).read(), 'html.parser')
blogList = soup.find('ul', {'id': 'elThumbnailResultArea'})

dls = blogList.find_all('dl')
url = []
title = []
date = []
info = []
for dl in dls:
    dt = dl.find('dt')
    a = dt.find('a')
    publishDate = dl.find('dd', {'class':'txt_inline'}).string
    article = Article(a['href'])
    info.append([a['href'], a['title'], article.text, publishDate])

info = json.dumps(info, ensure_ascii=False)
print(info)
