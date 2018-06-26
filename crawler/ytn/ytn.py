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

def crawl(url): #crawl with given url
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url).read(),'html.parser') #get html page
        for script in soup(['script', 'style']): #remove all scripts and styles
            script.extract()


        image = soup.find('meta', {'property': 'og:image'}) #get metatag image url
        img = str(image['content'])



        title = soup.find('div', {'class': 'article_tit'}).string # get title from soup

        publishDate = soup.find('div', {'extra_info'}).string # get published date
        matchDate = datefinder.find_dates(publishDate) # used datefinder python modules to extract only date
        published_at = ""
        for match in matchDate:
            if match:
                published_at = match
                break
        published_at = str(published_at)
        print(published_at)


        contentTag = soup.find('div', {'id': 'CmAdContent'}) #get content Tag 
        content = contentTag.get_text()


        name = r"[^ ]*[ ]?기자[ ]?" # get name of author before preprocess
        nameSearch = re.compile(name)
        authorNames = nameSearch.findall(content)
        authorName = ""
        for author in authorNames:
            if author and author != "기자" and author != "취재기자":
                authorName = author
                break

        print(authorName)


        content = preprocess(content) # normalize content
        contentList = [content] # make it to list
        result = predict_unseen_data(contentList, 'trained_model_14') # get category by deep learning model
        category = result[0]


        tr = TextRank(coef=1.0, window=5, content=content) # throw content to textrank class
        tr.sentence_rank() # extract sentences
        tr.keyword_rank() # extract keywords

        keywords = tr.keywords(num=3)
        keyword1 = ""
        keyword2 = ""
        keyword3 = ""
        sentence1 = ""
        sentence2 = ""
        sentence3= ""

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
            sentent2 = ""
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
        mediaName = "YTN"


        sql = "INSERT INTO `mediaNews` (`url`, `isSum`, `category`, `img`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, (url, isSum, category, img, mediaName, title, summarized, content, authorName, published_at, keyword1, keyword2, keyword3))

    except  Exception as e:
        print(e)
        sql = "INSERT INTO `mediaNews` (`url`, `errorflag`, `mediaName`) VALUES (%s, %s, %s)"
        curs.execute(sql, (url, 1, "YTN"))


if __name__ == '__main__':
    searchUrl = "http://www.ytn.co.kr/news/news_quick.php?page="
    conn = pymysql.connect(host='moyanews.c5hgfzyunggm.ap-northeast-2.rds.amazonaws.com', user='sysmetic', password='1q2w3e4r', db='newsData', charset='utf8', autocommit=True)
    curs = conn.cursor()

    while True:
        for i in range(10, 0, -1): # reverse range

            forsearch = searchUrl + str(i)

            soup = BeautifulSoup(urllib.request.urlopen(forsearch).read(), 'html.parser')
        
            for script in soup(['script', 'style']): # remove all scripts and styles
                script.extract()
                    
            newsList = soup.find('div', {'id' : 'ytn_list_v2014'})
            
            for a in newsList.find_all('a', href=True):
                url = 'http://www.ytn.co.kr' + a['href']
                sql = "SELECT id FROM mediaNews WHERE url='" + url + "'"
                curs.execute(sql)
                rows = curs.fetchall()
                if not rows:
                    crawl(url)
                else:
                    pass
                time.sleep(1)
        time.sleep(300)
