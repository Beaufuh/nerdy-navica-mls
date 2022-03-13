#Python 3.9.2

import requests
from bs4 import BeautifulSoup
import regex as re
import sys
import pandas as pd
import os
from datetime import datetime 

url = sys.argv[1]
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

address_s = soup.find_all('div', class_='pr-1 pl-1 d-xs-block d-md-inline float-md-right')
addresses = [i.text.replace('\n','') for i in address_s]

list_price_s = soup.find_all('div', class_='pr-1 pl-1 d-xs-block d-md-inline')
list_prices = []
for i in list_price_s:
	if 'List Price:' in i.text:
		list_prices.append(i.text.strip()[12:])

cost_categories = []
for i in list_prices:
	i = int(re.sub('[$,]','', i))
	# print(i)
	if i >= 200000:
		cost_categories.append('high')
	elif i < 200000 and i >= 100000:
		cost_categories.append('medium')
	elif i < 100000:
		cost_categories.append('low')	

data_dict = {
	'addresses': addresses,
	'list_prices': list_prices,
	'cost_categories': cost_categories
	}

if os.path.exists(r"./navica_data"):
	os.chdir(r"./navica_data")
else:
	os.mkdir(r"./navica_data")
	os.chdir(r"./navica_data")
now = datetime.now().strftime("%y-%m-%d %H-%M-%S")
df = pd.DataFrame.from_dict(data_dict)
df.to_excel(f'{now}.xlsx')


#create master datalist from all Navica data collected to date, not just this iteration.
df_list = []
for i in os.listdir():
	if not i == 'all_data.xlsx':
		df = pd.read_excel(i, index_col=0)
		df_list.append(df)

df = pd.concat(df_list).drop_duplicates()
df.to_excel('all_data.xlsx', index=False)



