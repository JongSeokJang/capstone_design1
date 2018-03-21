from django.shortcuts import render, redirect
from django.http import HttpResponse
import pymysql

# Create your views here.

def index(request):
    query = request.GET.get('query')
    userQuery = request.GET.get('userQuery')
    mariaId = request.GET.get('mariaId')
    if query and userQuery == "":
        conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * from mediaNews WHERE content LIKE " + "'%"+query+"%'"+" ORDER BY id DESC limit 9"
        curs.execute(sql)
        rows = curs.fetchall()
        if rows:
            mariaId = rows[-1]
            mariaId = mariaId['id']
        else:
            mariaId = -1
        userQuery = query
        sql = "SELECT mediaName,COUNT(*) as count FROM mediaNews GROUP BY mediaName ORDER BY count DESC"
        curs.execute(sql)
        count = curs.fetchall()
        conn.close()
        searchQuery = "검색 내용 : " + query
        if mariaId == -1:
            return redirect('/')
        else:
            return render(request, 'newsApp/index.html', {'rows': rows, 'counts': count, 'searchQuery': searchQuery, 'userQuery': userQuery, 'mariaId': mariaId})
    elif query == "" and userQuery:
        conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * from mediaNews WHERE content LIKE " + "'%"+userQuery+"%'"+" AND id < " + mariaId + " ORDER BY id DESC limit 9"
        curs.execute(sql)
        rows = curs.fetchall()
        if rows:
            mariaId = rows[-1]
            mariaId = mariaId['id']
        else:
            mariaId = -1
        query = userQuery
        sql = "SELECT mediaName,COUNT(*) as count FROM mediaNews GROUP BY mediaName ORDER BY count DESC"
        curs.execute(sql)
        count = curs.fetchall()
        conn.close()
        searchQuery = "검색 내용 : " + query
        if mariaId == -1:
            return redirect('/')
        else:
            return render(request, 'newsApp/index.html', {'rows': rows, 'counts': count, 'searchQuery': searchQuery, 'userQuery': userQuery, 'mariaId': mariaId})
    else:
        conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT mediaName,COUNT(*) as count FROM mediaNews GROUP BY mediaName ORDER BY count DESC"
        curs.execute(sql)
        count = curs.fetchall()
        conn.close()
        return render(request, 'newsApp/index.html', {'counts':count})
