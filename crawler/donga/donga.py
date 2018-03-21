from bs4 import BeautifulSoup
import urllib.request
import datefinder
import re
import datetime
from textrank import TextRank
import pymysql
import time
from preprocess import preprocess
import sys
sys.path.append('../')
from cnn_run import predict_unseen_data

def crawl(url):
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        for script in soup(['script', 'style']):
            script.extract()
        try:
            image = soup.find('meta', property='og:image')
            img = str(image['content'])
        except Exception as e:
            img = ''
            print(e)
        try:
            soup.find('div', {'class': 'articlePhotoR'}).decompose()
        except Exception as e:
            print(e)
        
        title = soup.find('h2', {'class': 'title'}).string
        try:
            soup.find('div', {'class': 'articlePhotoC'}).decompose()
        except Exception as e:
            print(e)

        try:
            soup.find('div', {'class': 'videotag-player vodatv'}).decompose()
        except Exception as e:
            print(e)

        try:
            author = soup.find('span', {'class': 'report'}).get_text()
            authorName = author
        except Exception as e:
            authorName = ''
            print(e)
        try:
            publishDate = soup.find('span', {'class': 'date01'}).string
            matchDate = datefinder.find_dates(publishDate)
            for match in matchDate:
                if match:
                    published_at = match
                    break
            published_at = str(published_at)
        except Exception as e:
            published_at = ''
            print(e)

        try:
            soup.find('strong', {'class': 'sub_title'}).decompose()
        except Exception as e:
            print(e)
        content = soup.find('div', {'class': 'article_txt'}).get_text()
        content = preprocess(content)
        contentList = [content]
        result = predict_unseen_data(contentList, 'trained_model_14')
        category = result[0]

        tr = TextRank(window=5, coef=1.0, content=content)
        tr.sentence_rank()
        tr.keyword_rank()

        isSum = '요약됨'
        summarized = ""
        i = 0
        for sentence in tr.sentences(ratio=0.4):
            if i == 3:
                break
            summarized = summarized + ' ' + sentence[0]
            i += 1
        if summarized == '':
            summarized = content
            isSum = ''
        keywordList = tr.keywords(num=3)
        keyword1 = keywordList[0][0]
        keyword2 = keywordList[1][0]
        keyword3 = keywordList[2][0]
        mediaName = "동아일보"
        if content:
            sql = "INSERT INTO `mediaNews` (`url`, `isSum`, `category`,`img`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            curs.execute(sql, (url, isSum, category, img, mediaName, title, summarized, content, authorName, published_at, keyword1, keyword2, keyword3))
            conn.commit()
 

    except Exception as e:
        print(e)


if __name__ == '__main__':
    searchUrl = "http://news.donga.com/List?p=2"
    conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
    curs = conn.cursor()
    while True:
        for i in range(0, 10):
            i = i * 2
            forsearch = searchUrl + str(i) + "1&prod=news&ymd=&m=NP"
            soup = BeautifulSoup(urllib.request.urlopen(forsearch).read(), 'html.parser')
            for script in soup(['script', 'style']):
                script.extract()

            newsList = soup.find('div', {'id': 'contents'})
            
            for a in newsList.find_all('a', href=True):
                url = a['href']
                sql = "SELECT id FROM mediaNews WHERE url='" + url + "'"
                curs.execute(sql)
                rows = curs.fetchall()
                if not rows:
                    crawl(url)
                else:
                    pass
                time.sleep(1)
            time.sleep(1)
        time.sleep(300)
