import urllib.request
from bs4 import BeautifulSoup
from textrank import TextRank
from preprocess import preprocess
import datefinder
import re
import pymysql
import time
import urllib
import sys
sys.path.append('../')
from cnn_run import predict_unseen_data




def crawl(url):
    try:
        mediaName = "한국경제"
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

        for script in soup(['script', 'style']):
            script.extract()
        try:
            image = soup.find('meta', {'property': 'og:image'})
            img = str(image['content'])
        except Exception as e:
            img = ''


        title = soup.find('h1', {'class': 'title'}).string
        
        try:
            author = soup.find('div', {'class': 'editor'}).get_text()
            author = author.replace('\n', '')
            author = author.replace('\t', '')
        except:
            author = ''
        authorName = author

        published_at = soup.find('span', {'class': 'time'}).string
        publishDate = published_at
        
        try:
            for div in soup.find_all('div',{'class': 'wrap_img'}):
                div.decompose()
        except:
            pass
        try:
            soup.find('div', {'class':'hk-news-link'}).decompose()
        except:
            pass
        try:
            soup.find('p', {'class':'copy'}).decompose()
        except:
            pass

        try:
            soup.find('div', {'class':'summary editoropinions'}).decompose()
        except:
            pass

        content = soup.find('div', {'class':'articlebody ga-view'}).get_text()
        content = preprocess(content)
        contentList = [content]
        result = predict_unseen_data(contentList, 'trained_model_14')
        category = result[0]


        tr = TextRank(window=5, coef=1.0, content=content)
        tr.sentence_rank()
        tr.keyword_rank()
        
        isSum = "요약됨"
        summarized = ''
        i = 0
        for sentence in tr.sentences(ratio=0.4):
            if i == 3:
                break
            summarized = summarized + " " + sentence[0]
            i += 1
        if summarized == '':
            summarized = content
            isSum = ''
        i = 0
        for keyword in tr.keywords(num=3):
            if i == 3:
                break
            if i == 0:
                keyword1 = keyword[0]
            if i == 1:
                keyword2 = keyword[0]
            if i == 2:
                keyword3 = keyword[0]
            i += 1


        #push to mariaDB
        sql = "INSERT INTO `mediaNews` (`url`, `isSum`, `category`, `img`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, (url, isSum, category, img, mediaName, title, summarized, content, author, publishDate, keyword1, keyword2, keyword3))
 
        conn.commit()
 


    except Exception as e:
        print(e)
if __name__ == '__main__':
    searchUrl = "http://news.hankyung.com/news?page="
    conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
    curs = conn.cursor()
    while True:
        for i in range(1,45):
            forsearch = searchUrl + str(i) + '&hkonly=true'
            soup = BeautifulSoup(urllib.request.urlopen(forsearch).read(), 'html.parser')
            lists = soup.find_all('ul', {'class': 'list_basic'})
            for l in lists:
                for a in l.find_all('a', href=True):
                    url = a['href']
                    elems = url.split('http://')
                    if len(elems) == 2:
                        root = elems[1].split('/')[0]
                    if url=='#':
                        pass
                    else:
                        sql = "SELECT id FROM mediaNews WHERE url='" + url + "'"
                        curs.execute(sql)
                        rows = curs.fetchall()
                        if not rows and root =='news.hankyung.com':
                            crawl(url)
                        else:
                            pass
                        time.sleep(0.1)
                    time.sleep(0.1)
                time.sleep(0.1)
            time.sleep(0.1)
        time.sleep(300)
