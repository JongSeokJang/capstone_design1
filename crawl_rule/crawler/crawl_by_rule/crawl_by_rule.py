from bs4 import BeautifulSoup
import urllib.request
import requests
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

#def crawl(rows):
def crawl(url):
    try:
        main_url = url.split('/')[2]
        sql = "SELECT mediaName, titleTag, contentTag, authorTag, publishdateTag, euckr FROM crawlingRule WHERE main_url='" + main_url + "'"
        curs.execute(sql)
        rows = curs.fetchall()
        print(rows)
        if not rows:
            pass

        rule = rows[0]
        mediaName = rule[0]
        titleTag = rule[1]
        contentTag = rule[2]
        authorTag = rule[3]
        publishdateTag = rule[4]
        euckr = rule[5]
        print(euckr)
        print(mediaName)

        if euckr == 'Y':
            response = requests.get(url)
            response.encoding = 'euc-kr'
            plainText = response.text
            soup = BeautifulSoup(plainText, "html.parser")
        else:
            response = requests.get(url)
            response.encoding = 'utf-8'
            plainText = response.text
            soup = BeautifulSoup(plainText, "html.parser")

        for script in soup(['script', 'style']): #remove scripts and styles
            script.extract()



        # initialize variables
        title = ""
        content = ""
        author = ""
        publishDate = ""
        sentence1 = ""
        sentence2 = ""
        sentence3 = ""
        summarized = ""
        keyword1 = ""
        keyword2 = ""
        keyword3 = ""
        img = ""


        #extract title
        try:
            if "#" in titleTag:
                division = titleTag.split('#')[0]
                id_n_css = titleTag.split('#')[1]
                tagID = id_n_css.split('.')[0]
                css = ' '.join(id_n_css.split('.')[1:])
                title = soup.find(division, {'id': tagID}).get_text()

            else:
                division = titleTag.split('.')[0]
                css = ' '.join(titleTag.split('.')[1:])
                title = soup.find(division, {'class': css}).get_text()
        except:
            pass

        print(title)
        
        #extract content
        try:
            if "#" in contentTag:
                division = contentTag.split('#')[0]
                id_n_css = contentTag.split('#')[1]
                tagID = id_n_css.split('.')[0]
                css = ' '.join(id_n_css.split('.')[1:])
                content = soup.find(division, {'id': tagID}).get_text()

            else:
                division = contentTag.split('.')[0]
                css = ' '.join(contentTag.split('.')[1:])
                content = soup.find(division, {'class': css}).get_text()
        except:
            pass

        #extract publishDate
        try:
            if "#" in publishdateTag:
                division = publishdateTag.split('#')[0]
                id_n_css = publishdateTag.split('#')[1]
                tagID = id_n_css.split('.')[0]
                css = ' '.join(id_n_css.split('.')[1:])
                publishDate = soup.find(division, {'id': tagID}).get_text()

            else:
                division = publishdateTag.split('.')[0]
                css = ' '.join(publishdateTag.split('.')[1:])
                publishDate = soup.find(division, {'class': css}).get_text()
        except:
            pass
        publishDate = publishDate.replace('.', '-')
        matchDate = datefinder.find_dates(publishDate)
        published_at = ""
        for match in matchDate:
            if match:
                published_at = match
                break
        published_at = str(published_at)




        #extract image
        try:
            image = soup.find('meta', {'property': 'og:image'}) #get metatag image url
            img = str(image['content'])
        except:
            pass



        #extract author
        try:
            if "#" in authorTag:
                division = authorTag.split('#')[0]
                id_n_css = authorTag.split('#')[1]
                tagID = id_n_css.split('.')[0]
                css = ' '.join(id_n_css.split('.')[1:])
                author = soup.find(division, {'id': tagID}).get_text()

            else:
                division = authorTag.split('.')[0]
                css = ' '.join(authorTag.split('.')[1:])
                author = soup.find(division, {'class': css}).get_text()
        except:
            pass

        name = r"[^ ]*[ ]?기자[ ]?" # get name of author before preprocess
        nameSearch = re.compile(name)
        authorNames = nameSearch.findall(author)
        authorName = ""
        for author in authorNames:
            if author and author != "기자" and author != "취재기자":
                authorName = author
                break



        #normalize content
        content = preprocess(content)


        #extract category by deep learning
        contentList = [content]
        result = predict_unseen_data(contentList, 'trained_model_14') # get category by deep learning model
        category = result[0]


        tr = TextRank(coef=1.0, window=5, content=content) # throw content to textrank class
        tr.sentence_rank() # extract sentences
        tr.keyword_rank() # extract keywords

        keywords = tr.keywords(num=3)
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
            summarized = content
            isSum = ""
        else:
            summarized = sentence1 + " " + sentence2 + " " + sentence3
            isSum = "요약됨"


        sql = "UPDATE mediaNews SET isSum = %s, category = %s, img = %s, mediaName = %s, title = %s, summarized = %s, content = %s, author = %s, publishDate = %s, keyword1 = %s, keyword2 = %s, keyword3 = %s WHERE url = %s"
        curs.execute(sql, (isSum, category, img, mediaName, title, summarized, content, authorName, published_at, keyword1, keyword2, keyword3, url))
        print("crawled!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    except Exception as e:
        sql = "UPDATE mediaNews SET errorflag=%s WHERE url = %s"
        curs.execute(sql, (1, url))
        print(e)





if __name__ == "__main__":
    conn = pymysql.connect(host='moyanews.c5hgfzyunggm.ap-northeast-2.rds.amazonaws.com', user="sysmetic", password="1q2w3e4r", db="newsData", charset="utf8", autocommit=True)
    curs = conn.cursor()

    while True:
        sql = "SELECT url FROM mediaNews WHERE content IS NULL AND errorflag=0 ORDER BY id ASC LIMIT 100"
        curs.execute(sql)

        rows = curs.fetchall()
        for row in rows:
            crawl(row[0])
            time.sleep(2)
        time.sleep(0.1)
