from django.shortcuts import render
import pymysql

# Create your views here.

def index(request):
    query = request.GET.get('query')
    if query:
        conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * from mediaNews WHERE content LIKE " + "'%"+query+"%'"+" ORDER BY publishDate DESC"
        curs.execute(sql)

        rows = curs.fetchall()
        conn.close()
        return render(request, 'newsApp/index.html', {'rows': rows})
    else:
        return render(request, 'newsApp/index.html', {})
