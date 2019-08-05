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
	i = i.replace("CF410A","")
	i = i.replace("CF411A","")
	i = i.replace("CF412A","")
	i = i.replace("CF413A","")
	i = i.replace("(","")
	i = i.replace(")","")
	i = i.replace("\u202c","")
	i = i.replace("\u202d","")
	i = i.replace("%","")
	i = i.replace("*","")
	return i

def hpToners(soup, ip, location):
	count = 0
	level = []

	for i in soup.body.findAll(text=re.compile('Order')):
		hpToner.append(hpSimplify(i))

	for tag in soup.find_all('td', "alignRight valignTop"):
		for i in tag.contents:
			percent = hpSimplify(i)
			if count == 0:
				color = 'Black'
			elif count == 1:
				color = 'Cyan'
			elif count == 2:
				color = 'Magenta'
			else:
				color = 'Yellow'

			try:
				if percent == "\xa0" or int(percent) <= 10:
					text = color + " is low/empty at " + str(location) + " (" + str(ip) + ") "
					text = text + "\n" + hpToner[count]
					toaster.show_toast("WARNING", text, duration=15)
					#level.append([color, percent])
				#else:
					#level.append([color, percent])

				count = count + 1
			except:
				print(location, ip)

	#for i in range(len(level)):
		#level[i].append(hpToner[i])

	#return level

def ricohToners(soup, ip, location):
	count = 0
	level = []
	temp = []
	stuff = []
	colorType = False

	for tag in soup.find_all("img"):
		stuff.append(tag)

	for tag in soup.find_all("dl"):
		for i in tag.contents:
			if i != "\n":
				temp.append(i)
				if "Cyan" in i:
					colorType = True

	if colorType == True:
		for i in range(len(stuff)):
			try:
				if 'bdr-1px-666' in stuff[i]['class']:
					if count == 0:
						color = 'Black'
					elif count == 1:
						color = 'Cyan'
					elif count == 2:
						color = 'Magenta'
					else:
						color = 'Yellow'

					ricohPercent = (int(stuff[i]['width'])/162)*100

					if  ricohPercent <= 10:
						text = color + " is low/empty at " + str(location) + " (" + str(ip) + ") "
						toaster.show_toast("WARNING", text, duration = 15)
						#level.append([color, "Warning"])
					#else:
						#level.append(["Wrong"])
					count += 1
			except:
				continue

			#return level

	else:
		for i in range(len(temp)):
			if "Black" in temp[i]:
				if "Status OK" not in temp[i+1]:
					toaster.show_toast("WARNING", "Black toner is low in " + str(location) + " (" + str(ip) + ") ", duration = 15)
					#level.append(["Black", "Warning"])
				#else:
					#level.append(["Black", "Status OK"])
				break

		#return level
			
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
		hpToners(soup, df['IP'][i], df['Location'][i])
	elif brands[i] == "Ricoh":
		#toner.append(ricohToners(soup, df['IP'][i], df['Location'][i]))
		ricohToners(soup, df['IP'][i], df['Location'][i])