from bs4 import BeautifulSoup
import urllib.request
import pymysql
import datefinder
from textrank import TextRank
from preprocess import preprocess

def crawl(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

    #get title
    title = soup.find('h3').string
    print(title)



if __name__ == '__main__':
    url = "http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=001&aid=0009957864"

    crawl(url)
