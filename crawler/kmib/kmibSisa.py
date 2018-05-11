from bs4 import BeautifulSoup
import urllib.request
import time
import datefinder
import re
from textrank import TextRank
import pymysql


def crawl(url):
    try:
        with open('url_list2.txt', 'a') as out:
            out.write(url+'\n')
        out.close()

        #mediaName
        mediaName = "국민일보"
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

        #Get title
        title = soup.find('h3').string
        #Get publishDate
        publishDate = soup.find('span', {'class' : 't11'}).string

        #Get content
        content = soup.find('div', {'class' : 'tx', 'id' : 'articleBody', 'itemprop' : 'articleBody'}).get_text()
        content = content.replace('\t', '')
        content = content.replace('\n', '')

        #Get author
        name = r"[^ ]*[ ]?기자[ ]?"
        nameSearch = re.compile(name)
        authorNames = nameSearch.findall(content)
        author = authorNames[0]

        #Get summarized
        tr = TextRank(window=5, coef=1.0, content=content)
        tr.keyword_rank()
        
        try:
            tr.sentence_rank()
            summarized = ""
            for sentence in tr.sentences(ratio=0.5):
                summarized = summarized + sentence[0]
        except:
            summarized = content

        i = 0
        for keyword in tr.keywords(ratio=0.9):
            if i == 3:
                break
            if i == 0:
                keyword1 = keyword[0]
            if i == 1:
                keyword2 = keyword[0]
            if i == 2:
                keyword3 = keyword[0]
            i+=1
        sql = "INSERT INTO `newsData` (`uri`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, (url, mediaName, title, summarized, content, author, publishDate, keyword1, keyword2, keyword3))
        #conn.commit()
        #conn.close()


    except Exception as e:
        print(e)


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='1q2w3e4r', db='newsData', charset='utf8', autocommit=True)
    curs = conn.cursor()
    while True:
        searchUrl = "http://news.kmib.co.kr/article/list.asp?sid1=all"
        mainUrl = "http://news.kmib.co.kr/article/"
        soup = BeautifulSoup(urllib.request.urlopen(searchUrl).read(), 'html.parser')

        news_list = soup.find('div', 'nws_list')
        aTag = news_list.find_all('a', href=True)
        fp = open('url_list2.txt', 'r')
        url_list = fp.readlines()

        i = 0
        for a in aTag:
            if i % 3 == 0:
                url = mainUrl + a['href']
                urlCheck = url + '\n'
                if urlCheck in url_list:
                    continue
                else:
                    crawl(url)
            i+=1
        fp.close()
        time.sleep(300)
