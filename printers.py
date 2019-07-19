from lxml import html
import requests
import urllib3
import re
from bs4 import BeautifulSoup
import pandas as pd

brands = []
urls = []

def readHtml(link):
    response = http.request('GET', link)
    bSoup = BeautifulSoup(response.data, 'lxml')
    return bSoup

def simplify(i):
    i = i.replace(" ","")
    i = i.replace("\n","")
    i = i.replace("†","")
    return i

http = urllib3.PoolManager()

df = pd.read_excel('printerIP.xlsx', sheet_name = 'Sheet1')

for i in df.index:
    brands.append(df['Brand'][i])
    ip = df['IP'][i]
    url = 'http://' + ip + '/'
    urls.append(url)

for i in range(len(urls)):
    if brands[i] = 'HP':
        soup = 

x = 0
level = []
for tag in soup.find_all('td', "alignRight valignTop"):
    for i in tag.contents:
        y = simplify(i)
        level.append([x,y])
        x = x + 1

for i in soup.body.findAll(text=re.compile('Cartridge')):
    print(simplify(i))
print(level)