from bs4 import BeautifulSoup
import urllib.request

url = "http://news.mk.co.kr/newsRead.php?sc=30000001&year=2018&no=5"

soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

contents = soup.find_all('div', {'class' : 'art_txt'})

print(contents)
