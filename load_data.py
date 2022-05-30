import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymongo
from urllib.parse import quote_plus
from pymongo import MongoClient
from datetime import date

current_date = date.today().isoformat()

# get Best selling from book store
def get_best_selling_list():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    res = requests.get("https://www.books.com.tw/web/sys_cebtopb/cebook?loc=subject_004", headers = headers)
    content = BeautifulSoup(res.text, 'html.parser')

    tags = content.find(class_="mod type02_m035 clearfix")
    tagList = tags.select('.main_wrap .type02_m035 .type02_bd-a')

    #table layout, date as PPI
    tagDict = {'title': [], 'author': [], 'price': [], 'date':[]}

    for t in tagList:
        tagDict['title'].append(t.select('a')[0].text) 
        tagDict['author'].append(t.select('a')[1].text)
        tagDict['price'].append(t.find('b').text)
        tagDict['price'].append(t.select('.price_a b:last-child')[-1].text)
        tagDict['date'].append(current_date)
     
    # table column
    df = pd.DataFrame.from_dict(tagDict)
    
    return df

    #remove default index column
    #df convert to CSV file
    #df.to_csv('booksScraper.csv', index = False )

def mongoConnect(username, password, ip):
    username = quote_plus(username)
    password = quote_plus(password)
    client = pymongo.MongoClient(ip)
    return client

def insertData():
    data_dict = get_best_selling_list()
    mycollection.insert_many(data_dict.apply(lambda x: x.to_dict(), axis=1).to_list())
    apply_count = mycollection.count_documents({})
    print("Insert ", apply_count, " rows success!")

def updateData():
    mycollection.delete_many({"date": current_date})
    print("Delete ", total_count, "rows success!")

mongoDBId = mongoDBId
mongoDBPwd = mongoDBPwd
connStr = "mongodb+srv://" + mongoDBId + ":" + mongoDBPwd + "@cluster0.fkroy.mongodb.net/sample_analytics?retryWrites=true&w=majority"

mydb = mongoConnect(mongoDBId, mongoDBPwd, connStr).marketing
mycollection = mydb.bookstore_best_selling #tablename
total_count = mycollection.count_documents({})

#Avoid insert duplicate data / monthly batch
if total_count > 1:
    updateData()
    insertData()
else: #Data Initial
    insertData()
    
