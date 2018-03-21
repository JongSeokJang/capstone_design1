import urllib.request
from bs4 import BeautifulSoup
import datefinder
import datetime
import time
import re
from textrank import TextRank
import pymysql
from preprocess import preprocess
import sys
sys.path.append('../')
from cnn_run import predict_unseen_data


def crawl(url):
    try:

        #Media Name
        mediaName="연합뉴스"


        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

        for script in soup(['script', 'style']):
            script.extract()


        #Get title
        title = soup.find('h1', {'class': 'tit-article'}).string
        try:
            image = soup.find('meta', {'property': 'og:image'})
            img = str(image['content'])
        except Exception as e:
            img = ''
        #Get publishDate
        publishDateRes = soup.find_all('em')
        publishDate = publishDateRes[1].string

        #Get content
        try:
            articleImg = soup.find_all('div', 'article-img')
            for d in articleImg:
                d.decompose()
        except:
            pass
        try:
            articleImg = soup.find_all('div', 'article-img img-p4')
            for de in articleImg:
                de.decompose()
        except:
            pass
        try:
            soup.find('p', 'adrs').decompose()
        except:
            pass
        try:
            soup.find('div',{'class': 'stit'}).decompose()
        except:
            pass

        content = soup.find('div', 'article')
        content = content.get_text()

        #Get author
        name = r"[^ ]*[ ]?기자[ ]?"
        nameSearch = re.compile(name)
        authorNames = nameSearch.findall(content)
        author = authorNames[0]

        content = preprocess(content)
        content = content.replace('(춘천=연합뉴스)  =', '')
        content = content.replace('(제주=연합뉴스)  =', '')
        content = content.replace('(서울=연합뉴스)  =', '')
        content = content.replace('(대전=연합뉴스)  =', '')
        content = content.replace('(평창=연합뉴스)  =', '')
        content = content.replace('(군산=연합뉴스)  =', '')
        content = content.replace('(군위=연합뉴스)  =', '')
        content = content.replace('(구미=연합뉴스)  =', '')
        content = content.replace('(밀양=연합뉴스)  =', '')
        content = content.replace('(부산=연합뉴스)  =', '')
        content = content.replace('(청주=연합뉴스)  =', '')
        content = content.replace('(울산=연합뉴스)  =', '')
        content = content.replace('(통영=연합뉴스)  =', '')
        content = content.replace('(대구=연합뉴스)  =', '')
        content = content.replace('(수원=연합뉴스)  =', '')
        content = content.replace('(양산=연합뉴스)  =', '')
        content = content.replace('(안산=연합뉴스)  =', '')
        content = content.replace('(광주=연합뉴스)  =', '')
        content = content.replace('(하동=연합뉴스)  =', '')
        content = content.replace('(김제=연합뉴스)  =', '')
        content = content.replace('(전북=연합뉴스)  =', '')
        content = content.replace('(보령 공주=연합뉴스)  =', '')
        content = content.replace('(함평=연합뉴스)  =', '')
        contentList = [content]
        result = predict_unseen_data(contentList, 'trained_model_14')
        category = result[0]


        #Get summarzied
        tr = TextRank(window=5, coef=1.0, content=content)
        tr.sentence_rank()
        tr.keyword_rank()

        isSum = "요약됨"
        summarized = ""
        i = 0
        for sentence in tr.sentences(ratio=0.4):
            if i == 3:
                break
            summarized = summarized + " " + sentence[0]
            i += 1
        if summarized == '':
            summarized = content

            isSum = ''

        #Get keyword
        index = 0
        for keyword in tr.keywords(num=3):
            if index == 3:
                break
            if index == 0:
                keyword1 = keyword[0]
            if index == 1:
                keyword2 = keyword[0]
            if index == 2:
                keyword3 = keyword[0]
            index+=1
            

        sql = "INSERT INTO `mediaNews` (`url`, `isSum`, `category`, `img`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, (url, isSum, category, img, mediaName, title, summarized, content, author, publishDate, keyword1, keyword2, keyword3))
        
        conn.commit()
        
    except Exception as error:
        print(error)



if __name__ == '__main__':
    forSearchUrl = "http://www.yonhapnews.co.kr/society/07060000"
    conn = pymysql.connect(host='localhost', user='root', password='1q2w3e4r', db='newsData', charset='utf8')
    curs = conn.cursor()
    while True:
        for i in range(1,20):
            searchUrl = forSearchUrl + str(i).zfill(2) + ".html"
            soup = BeautifulSoup(urllib.request.urlopen(searchUrl).read(), 'html.parser')
            test1 = soup.find_all('div', 'con')
            for test in test1:
                for a in test.find_all('a', href=True):
                    url = a['href']
                    sql = "SELECT id FROM mediaNews WHERE url='" + url + "'"
                    curs.execute(sql)
                    rows = curs.fetchall()
                    if not rows:
                        crawl(url)
                    else:
                        pass
                    time.sleep(0.1)
                time.sleep(0.1)
            time.sleep(0.1)
        time.sleep(120)
