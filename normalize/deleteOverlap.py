import pymysql
import time
if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='root', password='1q2w3e4r', db='newsData', charset='utf8', autocommit=True)
    curs = conn.cursor()
    while True:
        sql = "DELETE FROM mediaNews WHERE id not in (SELECT id FROM (SELECT id FROM mediaNews GROUP BY title) as b)"
        curs.execute(sql)
        print("finished")
        time.sleep(200)
