## Author: Andrey Suvorov
## Date: 12/01/2023
import sqlite3 as sql
import requests
from bs4 import BeautifulSoup
import csv
import os.path


def html_file(URLs):
    print("HTML 文件获取")
    n = 0
    for URL in URLs:
        n = n+1
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser") 
        with open("{}_output.html".format(n), "w", encoding = 'utf-8') as file:
            file.write(str(soup.prettify()))

con = sql.connect('region.db')

if os.path.isfile('region.db'):
    print ("Database File exist")
else:
    con = sql.connect('region.db')
    with con:
        con.execute("""
        CREATE TABLE USER (
            region TEXT,
            client TEXT,
            link STRING PRIMARY KEY); """)
    con.commit()

cursor = con.cursor()
cursor.execute('SELECT link FROM USER WHERE region = "UZ" AND client = "mediapark"')
row = cursor.fetchall()
## print(row[0])
## rows = list(row)
for i, rows in enumerate(row):
    row[i] = rows[0]

def data_collect(URLs):
    print("设备信息和价格信息获取中...")
    csv_report = open('price_monitoring_W1.csv', 'w')
    write_file = csv.writer(csv_report)
    for URL in URLs:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        device_group = soup.find('div', {"class": "Catalog-information-right-block-left-center-info"}).h4
        price_group = soup.find('div', {"class": "Catalog-information-right-block-right-main"}).h1
        avaliable_group = soup.find('div', {"class": "Catalog-information-right-block-right-main"}).h4
        if price_group == None:
            data = [device_group.text, avaliable_group.text]
            print(device_group.text, avaliable_group.text)
            write_file.writerow(data)
        else: 
            data = [device_group.text, price_group.text]
            print(device_group.text, price_group.text)
            write_file.writerow(data)
    csv_report.close()

data_collect(row)


## URLs = [device_1, device_na]
## html_file(URLs)
## data_collect(URLs)
## data_collect(URLs,True)











