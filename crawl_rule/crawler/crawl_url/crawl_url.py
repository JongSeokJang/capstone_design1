from bs4 import BeautifulSoup
import urllib.request
import pymysql
import time

conn = pymysql.connect(host="moyanews.c5hgfzyunggm.ap-northeast-2.rds.amazonaws.com", user="sysmetic", password="1q2w3e4r", db="newsData", charset="utf8", autocommit=True)
curs = conn.cursor()

while True:
    sql = "SELECT url, urlTag, mainUrl FROM url_Rule"
    curs.execute(sql)
    rows = curs.fetchall()


    for row in rows:
        url = row[0]
        urlTag = row[1]
        mainUrl = row[2]

        soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

        for script in soup(['script', 'style']):
            script.extract()


        division = ""
        id_n_css = ""
        tagID = ""
        css = ""
        flag = 1
        if "#" in urlTag:
            division = urlTag.split('#')[0]
            id_n_css = urlTag.split('#')[1]
            tagID = id_n_css.split('.')[0]
            css = ' '.join(id_n_css.split('.')[1:])
            flag = 1
        else:
            division = urlTag.split('.')[0]
            css = ' '.join(urlTag.split('.')[1:])
            flag = 0

        newsList = ""
        if flag == 1:
            newsList = soup.find(division, {'id': tagID})
        elif flag == 0:
            newsList = soup.find(division, {'class': css})


        try:
            print("will get a tags")
            for a in newsList.find_all('a', href=True):
                url2 = mainUrl + a['href']
                print(url2)
                try:
                    sql = "SELECT id FROM mediaNews WHERE url='" + url2 + "'"
                    curs.execute(sql)
                    rows = curs.fetchall()
                    if not rows:
                        sql = "INSERT INTO mediaNews (url, errorflag) VALUES (%s, %s)"
                        curs.execute(sql, (url2, 0))
                except Exception as e:
                    print(e)
                    continue
                time.sleep(0.1)
            time.sleep(0.1)
        except Exception as e:
            print(e)
            continue
        time.sleep(1)
