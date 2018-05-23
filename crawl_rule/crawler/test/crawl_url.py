from bs4 import BeautifulSoup
import urllib.request
import time

url = "http://news.mk.co.kr/newsList.php?sc=30000001"

soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

for script in soup(['script', 'style']):
    script.extract()


urlTag = "div.list_area"
division = ""
id_n_css = ""
tagID = ""
css = ""
flag = 1
mainUrl=""
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
except Exception as e:
    print(e)
