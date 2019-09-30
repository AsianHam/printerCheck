from multiprocessing import Pool
import multiprocessing as mp
import pandas as pd
import time
import os
import re

brands = []
cmds = []
counter = 0

toaster = ToastNotifier()

df = pd.read_excel('yardPrinterIP.xlsx', sheet_name = 'Sheet1')

def ricohToners(cmd, ip, location):
	black = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.9.1.1").read()
	bLevel = re.sub("[^0-9]", "", black[-4:-1])

	if str(black):
		cyan = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.9.1.3").read()
		cLevel = re.sub("[^0-9]", "", cyan[-4:-1])

		if str(cyan):
			magenta = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.9.1.4").read()
			mLevel = re.sub("[^0-9]", "", magenta[-4:-1])
			yellow = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.9.1.5").read()
			yLevel = re.sub("[^0-9]", "", yellow[-4:-1])
			
			if int(bLevel) < 10:
				text = "Black is low/empty at " + ip + " " + location
				print(text)
			if int(cLevel) < 10:
				text = "Cyan is low/empty at " + ip + " " + location
				print(text)
				text = "Magenta is low/empty at " + ip + " " + location
				print(text)
			if int(yLevel) < 10:
				text = "Yellow is low/empty at " + ip + " " + location
				print(text)
		else:
			if int(bLevel) < 10:
				text = "Black is low/empty at " + ip + " " + location
				print(text)
	else:
		text = "Check " + ip + " " + location
		print(text)

def hpToners(cmd, ip, location):
	black = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.9.1.1").read()
	bLevel = re.sub("[^0-9]", "", black[-4:-1])
	order = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.6.1.1").read()
	order = order[-6:-2]
	
	if str(black):
		cyan = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.9.1.2").read()
		cLevel = re.sub("[^0-9]", "", cyan[-4:-1])

		if str(cyan):
			magenta = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.9.1.3").read()
			mLevel = re.sub("[^0-9]", "", magenta[-4:-1])
			yellow = os.popen(cmd + " 1.3.6.1.2.1.43.11.1.1.9.1.4").read()
			yLevel = re.sub("[^0-9]", "", yellow[-4:-1])

			if int(bLevel) < 10:
				text = "Black is low/empty at " + ip + " " + location + "\n" + order
				print(text)

			if int(cLevel) < 10:
				text = "Cyan is low/empty at " + ip + " " + location + "\n" + order
				print(text)

			if int(mLevel) < 10:
				text = "Magenta is low/empty at " + ip + " " + location + "\n" + order
				print(text)

			if int(yLevel) < 10:
				text = "Yellow is low/empty at " + ip + " " + location + "\n" + order
				print(text)
		else:
			if int(bLevel) < 10:
				text = "Black is low/empty at " + ip + " " + location + "\n" + order
				print(text)
	else:
		text = "Check " + ip + " " + location
		print(text)

def main(cmds):
	cmd = cmds[0]
	i = cmds[1]
	brands = cmds[2]

	if brands == 'Ricoh':
		ricohToners(cmd, str(df['IP'][i]), str(df['Location'][i]))
	elif brands == 'HP':
		hpToners(cmd, str(df['IP'][i]), str(df['Location'][i]))

if __name__ == "__main__":
	startTime = time.time()

	for i in df.index:
		brands.append(df['Brand'][i])
		ip = df['IP'][i]
		if brands[i] == 'Ricoh':
			cmd = "snmpwalk -v1 -c public " + ip
			cmds.append([cmd, counter, str(brands[i])])
		elif brands[i] == 'HP':
			cmd = "snmpwalk -v1 -c public " + ip
			cmds.append([cmd, counter, str(brands[i])])
		counter += 1

	with Pool(mp.cpu_count()) as p:
		records = p.map(main, cmds)
		p.terminate()
		p.join()

	print("Finished")
	print("--- %s seconds ---" % (time.time() - startTime))