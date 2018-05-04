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
        """Step 1: Get html"""
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        try:
            for script in soup(['script', 'style']):
                script.extract()
        except:
            pass
        try:
            for div in soup.find_all('div', {'class': 'center_img'}):
                div.decompose()
        except:
            pass

        '''
        Step 2: Get Title
        return title
        '''
        title = soup.find(id='title_text')
        title = title.string

        '''
        Step 3: Get publish date
        return published_at
        '''
        publishDateRes = soup.find(id='date_text')
        publishDate = publishDateRes.string
        matchDate = datefinder.find_dates(publishDate)
        for match in matchDate:
            if match:
                published_at = match
                break
        published_at = str(published_at)


        '''
        Step 4: Get author
        return authorName
        '''
        name = r"[^ ]*[ ]?기자[ ]?"
        nameSearch = re.compile(name)
        authorRes = soup.find(id='j1')
        author  = authorRes.get_text()
        authorNames = nameSearch.findall(author)
        for authorName in authorNames:
            if authorName:
                authorName = authorName.replace('\r\n\t\t\t\t', '')
                break
        soup.find('div', {'class':'date_ctrl_2011'}).decompose()
        image = soup.find('meta', property='og:image')
        img = str(image['content'])
        '''
        Step 5: Get content
        return content
        '''

        contentRes = soup.find(id='article_2011')
        content = contentRes.get_text()
        content = preprocess(content)
        contentList = [content]
        result = predict_unseen_data(contentList, 'trained_model_14')
        category = result[0]
        '''
        Step 6: Get summarized and keywords
        return summarized, keyword1, keyword2, keyword3
        '''

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
        mediaName = "조선비즈"
        if summarized == '':
            pass
        else:
            sql = "INSERT INTO `mediaNews` (`url`, `isSum`, `category`,`img`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            curs.execute(sql, (url, isSum, category, img, mediaName, title, summarized, content, authorName, published_at, keyword1, keyword2, keyword3))
            #conn.commit()
        

    except Exception as e:
        print(e)

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='1q2w3e4r', db='newsData', charset='utf8', autocommit=True)
    curs = conn.cursor()
    while True:
        searchUrl = 'http://biz.chosun.com/svc/list_in/list.html?pn='

        mainUrl = 'http://biz.chosun.com'
        for i in range(1, 20):
            forsearch = searchUrl + str(i)
            soup = BeautifulSoup(urllib.request.urlopen(forsearch).read(), 'html.parser')
            list1 = soup.find('div', 'list_vt')
            for a in list1.find_all('a', href=True):
                url = mainUrl + a['href']
                sql = "SELECT id FROM mediaNews WHERE url='" + url + "'"
                curs.execute(sql)
                rows=curs.fetchall()
                if not rows:
                    crawl(url)
                else:
                    pass
        time.sleep(300)
