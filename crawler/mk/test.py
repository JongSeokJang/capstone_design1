from bs4 import BeautifulSoup
import pymysql
import urllib.request
import time
import datefinder
import re
import datetime
import os
from textrank import TextRank
import chardet

def crawl(url, num):
    try:
        #media name
        mediaName = "매일경제"
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        #Get title
        title = soup.find('h1', {'class' : 'top_title'}).string
        title = str(title)
        print(chardet.detect(title))


        #Get author
        try:
            author = soup.find('li', {'class' : 'author'}).string
            author = str(author)
            print(chardet.detect(author))
        except:
            author = ""

        #Get publishDate
        try:
            publishDates = soup.find('li', {'class' : 'lasttime'}).get_text()
            matches = datefinder.find_dates(publishDates)
            for match in matches:
                publishDate = match
                break
        except:
            publishDate = ""



        #Get content
        try:
            content = ""
            contents = soup.find_all('div', 'art_txt')
            for c in contents:
                content = content + c.get_text()

            name = r"[^ ]*[ ]?기자[ ]?"
            nameSearch = re.compile(name)
            authorNames = nameSearch.findall(content)
            
            for authorName in authorNames:
                content = content.replace(authorName, '')
            
            content = content.replace('ⓒ 매일경제 & mk.co.kr, 무단전재 및 재배포 금지', '')
            content = content.replace('[]', '')        
            print(content)
            content = str(content)
            print(chardet.detect(content))
            num += 1
        except:
            content = ""

        return num

    except Exception as e:
        print(e)
        return num


if __name__ == '__main__':
    num = 1
    while True:
        now = datetime.datetime.now()
        nowYear = now.strftime('%Y')
        yearFile = nowYear + '.txt'
        url = "http://news.mk.co.kr/newsRead.php?sc=20000001&year=" + nowYear + "&no="

        if os.path.exists(yearFile):
            fp = open(yearFile, 'r')
            num = fp.readline()
            num = int(num)
            fp.close()
            searchUrl = url + str(num)
            print(searchUrl)
            num = crawl(searchUrl, num)
            fp2 = open(yearFile, 'w')
            fp2.write('%d'%num)
            fp2.close()
        else:
            fp = open(yearFile, 'w+')
            num = 1
            fp.write('%d'%num)
            fp.close()
