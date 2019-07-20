from lxml import html
import requests
import urllib3
import re
from bs4 import BeautifulSoup
import pandas as pd
from win10toast import ToastNotifier

brands = []
urls = []
level = []
hpToner = []
count = 0

toaster = ToastNotifier()

def readHtml(link):
    response = http.request('GET', link)
    bSoup = BeautifulSoup(response.data, 'lxml')
    return bSoup

def hpSimplify(i):
	i = i.replace(" ","")
	i = i.replace("\n","")
	i = i.replace("†","")
	i = i.replace("Order‭410A","")
	i = i.replace("(","")
	i = i.replace(")","")
	i = i.replace("\u202c","")
	return i

http = urllib3.PoolManager()

df = pd.read_excel('printerIP.xlsx', sheet_name = 'Sheet1')

for i in df.index:
    brands.append(df['Brand'][i])
    ip = df['IP'][i]
    url = 'http://' + ip + '/'
    urls.append(url)

for i in range(len(urls)):
    if brands[i] == 'HP':
        soup = readHtml(urls[i])

for tag in soup.find_all('td', "alignRight valignTop"):
	for i in tag.contents:
		percent = hpSimplify(i)
		if count == 0:
			color = 'black'
		elif count == 1:
			color = 'cyan'
		elif count == 2:
			color = 'magenta'
		else:
			color = 'yellow'

		level.append([color, percent])
		count = count + 1

for i in soup.body.findAll(text=re.compile('CF')):
	hpToner.append(hpSimplify(i))

for i in range(len(level)):
	level[i].append(hpToner[i])

print(level)

toaster.show_toast("Sample Notification", "Python is awesome!!")