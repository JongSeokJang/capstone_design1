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

        title = soup.find('h1', {'id':'news_title_text_id'}).string

        for div in soup.find_all('div', {'class': 'news_imgbox heightlong center'}):
            div.decompose()
        try:
            image = soup.find('meta', {'property': 'og:image'})
            img = str(image['content'])
        except Exception as e:
            img = ''
        #Get author name
        name = r"[^ ]*[ ]?기자[ ]?"
        nameSearch = re.compile(name)
        authorRes = soup.find(id='j1')
        try:
            author = authorRes.get_text()
            authorNames = nameSearch.findall(author)
            for authorName in authorNames:
                if authorName:
                    authorName = authorName.replace('\r\n\t\t\t\t', '')
                    authorName = authorName.replace('\n', '')
                    authorName = authorName.replace('\t', '')
                    break
        except:
            authorName = ''
            pass

        publishDate = soup.find('p', {'id': 'date_text'}).string
        matchDate = datefinder.find_dates(publishDate)
        for match in matchDate:
            if match:
                published_at = match
                break
        published_at = str(published_at)

        soup.find('div', {'class': 'date_ctrl_2011'}).decompose()
        soup.find('h3', {'class': 'news_subtitle'}).decompose()

        content = soup.find('div', {'id': 'news_body_id'}).get_text()
        content = preprocess(content)
        contentList = [content]
        result = predict_unseen_data(contentList, 'trained_model_14')
        category = result[0]


        tr = TextRank(window=5, coef=1.0, content=content)
        tr.sentence_rank()
        tr.keyword_rank()
        
        isSum = "요약됨"

        summarized = ""
        i = 0
        for sentence in tr.sentences(ratio=0.4):
            if i == 3:
                break
            if "▲" not in sentence:
                summarized = summarized + " " + sentence[0]
            i += 1
        if summarized == '':
            isSum = ''
            summarized = content
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
        mediaName = "조선일보"

        

        #push to mariaDB
        sql = "INSERT INTO `mediaNews` (`url`, `isSum`, `category`, `img`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, (url, isSum, category, img, mediaName, title, summarized, content, authorName, published_at, keyword1, keyword2, keyword3))
        conn.commit()
 

    except Exception as e:
        print(e)
    


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='1q2w3e4r', db='newsData', charset='utf8')
    curs = conn.cursor()
    while True:
        searchUrl = 'http://news.chosun.com/svc/list_in/list.html?pn='
        for i in range(1,70):
            forsearch = searchUrl + str(i)
            soup = BeautifulSoup(urllib.request.urlopen(forsearch).read(), 'html.parser')
            list1 = soup.find('div', {'id': 'list_area'})
            for a in list1.find_all('a', href=True):
                url = a['href']

                sql = "SELECT id FROM mediaNews WHERE url='" + url + "'"
                curs.execute(sql)
                rows = curs.fetchall()
                if not rows:
                    crawl(url)
                else:
                    pass
                
                time.sleep(0.1)
            time.sleep(10)
        time.sleep(30)
