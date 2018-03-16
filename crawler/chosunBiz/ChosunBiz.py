from bs4 import BeautifulSoup
import urllib.request
import datefinder
import re
import datetime
from textrank import TextRank
import pymysql
import time
from preprocess import preprocess

def preTreatment(content):
    content = content.replace('▲  금융위원회 제공', '')
    content = content.replace('▲금융위원회 제공', '')
    content = content.replace('▲ 삼성디스플레이 제공', '')
    content = content.replace('▲  삼성디스플레이 제공', '')
    return content

def crawl(url):
    try:
        """Step 1: Get html"""
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        for script in soup(['script', 'style']):
            script.extract()

        for div in soup.find_all('div', {'class': 'center_img'}):
            div.decompose()

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
        '''
        Step 6: Get summarized and keywords
        return summarized, keyword1, keyword2, keyword3
        '''

        tr = TextRank(window=5, coef=1.0, content=content)
        tr.sentence_rank()
        tr.keyword_rank()

        summarized = ""
        i = 0
        for sentence in tr.sentences(ratio=0.4):
            if i == 3:
                break
            if "▲" not in sentence:
                summarized = summarized + " " + sentence[0]
            i += 1
        if summarized == '':
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
            i+=1
        mediaName = "조선일보"
        sql = "INSERT INTO `mediaNews` (`url`, `img`, `mediaName`, `title`, `summarized`, `content`, `author`, `publishDate`, `keyword1`, `keyword2`, `keyword3`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        curs.execute(sql, (url, img, mediaName, title, summarized, content, authorName, published_at, keyword1, keyword2, keyword3))
        conn.commit()
        

    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        searchUrl = 'http://biz.chosun.com/svc/list_in/list.html?pn='

        mainUrl = 'http://biz.chosun.com'
        
        conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
        curs = conn.cursor()
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
