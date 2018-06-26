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
            soup.find('div', {'class': 'article_relation'}).decompose()
        except Exception as e:
            print(e)
        try:
            for b in soup(['b']):
                b.extract()
        except Exception as e:
            print(e)
        try:
            videos = soup.find_all('div', {'class':'jp-player-bg'})
            for video in videos:
                video.decompose()
        except Exception as e:
            print(e)
        try:
            image = soup.find('meta', property='og:image')
            img = str(image['content'])
        except Exception as e:
            img = ''
            print(e)
        try:
            soup.find('div', {'id':'aside'}).decompose()
        except Exception as e:
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

        tr = TextRank(coef=1.0, window=5, content=content)
        tr.sentence_rank()
        tr.keyword_rank()
        keywords = tr.keywords(num=3)
        keyword1 = ''
        keyword2 = ''
        keyword3 = ''

        if len(keywords) > 0:
            keyword1 = keywords[0][0]
        if len(keywords) > 1:
            keyword2 = keywords[1][0]
        if len(keywords) > 2:
            keyword3 = keywords[2][0]


        trSentence = tr.sentences(ratio=0.4)
        if len(trSentence) > 0 and trSentence[0][0]:
            sentence1 = trSentence[0][0]
            sentence1 = sentence1.replace('하지만', '')
            sentence1 = sentence1.replace('그러나', '')
        else:
            sentence1 = ""
        if len(trSentence) > 1 and trSentence[1][0]:
            sentence2 = trSentence[1][0]
            sentence2 = sentence2.replace('하지만', '')
            sentence2 = sentence2.replace('그러나', '')
        else:
            sentence2 = ""
        if len(trSentence) > 2 and trSentence[2][0]:
            sentence3 = trSentence[2][0]
            sentence3 = sentence3.replace('하지만', '')
            sentence3 = sentence3.replace('그러나', '')
        else:
            sentence3 = ""
        if sentence1 == "":
            summarzied = content
            isSum = ""
        else:
            summarized = sentence1 + " " + sentence2 + " " + sentence3
            isSum = "요약됨"
        sql = "INSERT INTO `mediaNews` (`url`, `isSum`, `category`,`img`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, (url, isSum, category, img, mediaName, title, summarized, content, authorName, published_at, keyword1, keyword2, keyword3))
        #conn.commit()
 

    except Exception as e:
        print(e)


if __name__ == '__main__':
    searchUrl = "http://news.donga.com/List?p=2"
    conn = pymysql.connect(host='localhost', user='root', password='1q2w3e4r', db='newsData', charset='utf8', autocommit=True)
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
