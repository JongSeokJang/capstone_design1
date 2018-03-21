from bs4 import BeautifulSoup
import urllib.request
import re


def get_encoding(soup):
    encod = soup.meta.get('charset')
    if encod == None:
        encod = soup.meta.get('content-type')
        if encod == None:
            content = soup.meta.get('content')
            match = re.search('charset=(.*)', content)
            if match:
                encod = match.group(1)
            else:
                raise ValueError('unable to find encoding')
    return encod

url = "http://news.mk.co.kr/newsRead.php?sc=20000001&year=2018&no=1"

soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

for script in soup(['script', 'style']):
    script.extract()



encod = get_encoding(soup)

if encod == 'euc-kr':
    content = soup.find('div', {'class' : 'art_txt'}).string
    #content = content.encode('euc-kr')
    print(content)

else:
    print("this is utf8")



