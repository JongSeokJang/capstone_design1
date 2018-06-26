import pymysql
import time
from textblob import TextBlob
from googletrans import Translator
import json
from preprocess import preprocess


def analyze(rows, translator):
    for row in rows:
        try:
            ID = row[0]
            content = row[1]
            content = preprocess(content)

            english_content = translator.translate(content)
            english_content = english_content.text

            analysis = TextBlob(english_content)
            polarity = analysis.sentiment.polarity
            sentiment = float(polarity) * 10
            sentiment = sentiment * 2
            sentiment = round(sentiment)
            if sentiment > 10:
                sentiment = 10
            if sentiment < -10:
                sentiment = -10
            sql = "UPDATE mediaNews SET sentiment = %s  WHERE id="+str(ID)
            curs.execute(sql, (sentiment))
        except:
            sql = "UPDATE mediaNews SET errorflag = 1 WHERE id=" + str(ID)
            curs.execute(sql)



if __name__=='__main__':
    conn = pymysql.connect(host="moyanews.c5hgfzyunggm.ap-northeast-2.rds.amazonaws.com", user="sysmetic", password="1q2w3e4r", db="newsData", charset="utf8", autocommit=True)
    curs = conn.cursor()
    translator = Translator()

    while True:
        sql = "SELECT id, content, title FROM mediaNews WHERE sentiment IS NULL AND errorflag=0 AND id%2=0 LIMIT 20"
        curs.execute(sql)
        rows = curs.fetchall()

        if not rows:
            time.sleep(10)
        else:
            analyze(rows, translator)
