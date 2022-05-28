import requests
from bs4 import BeautifulSoup
import pandas as pd

# get Best selling from book store
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
res = requests.get("https://www.books.com.tw/web/sys_cebtopb/cebook?loc=subject_004", headers = headers)
content = BeautifulSoup(res.text, 'html.parser')

tags = content.find(class_="mod type02_m035 clearfix")
tagList = tags.select('.main_wrap .type02_m035 .type02_bd-a')

#table layout
tagDict = {'title': [], 'author': [], 'price': []}

for t in tagList:
    tagDict['title'].append(t.select('a')[0].text) 
    tagDict['author'].append(t.select('a')[1].text)
    tagDict['price'].append(t.find('b').text)
     
# table column
df = pd.DataFrame.from_dict(tagDict)

#remove default index column
#Save data as CSV files
df.to_csv('booksScraper.csv', index = False )
