from lxml import html
import requests
import urllib3
import re
from bs4 import BeautifulSoup
import pandas as pd
from win10toast import ToastNotifier

brands = []
urls = []
hpToner = []
toner = []

toaster = ToastNotifier()

http = urllib3.PoolManager()

df = pd.read_excel('printerIP.xlsx', sheet_name = 'Sheet1')

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

def hpToners(soup):
	count = 0
	level = []
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

	return level

def ricohToners(soup):
	count = 0
	level = []
	for tag in soup.find_all("img", "ver-algn-m"):
		for i in tag.contents:
			print(i)
			
for i in df.index:
	brands.append(df['Brand'][i])
	ip = df['IP'][i]
	if brands[i] == "HP":
		url = 'http://' + ip + '/'
		urls.append(url)
	elif brands[i] == "Ricoh":
		url = ip + "/web/guest/en/websys/webArch/getStatus.cgi#linkToner',000"
		urls.append(url)

for i in range(len(urls)):
	soup = readHtml(urls[i])
	if brands[i] == 'HP':
		toner.append(hpToners(soup))
	elif brands[i] == "Ricoh":
		toner.append(ricohToners(soup))


print(toner)

toaster.show_toast("Sample Notification", "Python is awesome!!")