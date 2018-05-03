# Capstone design Project

## WEB DEMO
http://moya.ai/news

## Members ...
- 장종석
- 이상협
- 유승재

## Goal
이번 캡스톤 디자인 목표는 각 언론사의 뉴스를 실시간으로 크롤링하여 요약해서 정보 전달을 해주는 아이폰 어플을 만드는 것을 목표로 한다.

### requirements
- python3
- pip3
- mariaDB

### prerequisites (python3 modules)
- django
- networkx
- nltk
- BeautifulSoup4
- datefinder

### how to install python3 modules
- django : pip3 install django
- networkx : pip3 install networkx
- nltk installation is done as followed
```python3
pip3 install nltk (in terminal)
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
```
- BeautifulSoup4 : pip3 install BeautifulSoup4
- datefinder : pip3 install datefinder

### how to start web demo in local
brief demo for making iphone application
- IN LOCAL
```
python3 manage.py runserver
```

- IN WEB
Fix ALLOWED_HOSTS in settings.py location :capstone_design1/sysmeticWeb/sysmeticWeb/
```
example
ALLOWED_HOSTS = ['13.125.229.40', 'localhost']
```

# CRITICAL
It is critical to fix password to corresponding password in server or local etc..
Fix passwords in crawler files and views

### crawler password src location example
- capstone_design1/crawler/donga/donga.py
```
if __name__ == '__main__':
    searchUrl = "http://news.donga.com/List?p=2"
    conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
    curs = conn.cursor()

```
### views password src location
- capstone_design1/sysmeticWeb/newsApp/views.py
```
def index(request):
    query = request.GET.get('query')
    userQuery = request.GET.get('userQuery')
    mariaId = request.GET.get('mariaId')
    if query and userQuery == "":
        conn = pymysql.connect(host='localhost', user='root', password='', db='newsData', charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * from mediaNews WHERE content LIKE " + "'%"+query+"%'"+" ORDER BY id DESC limit 9"

```
