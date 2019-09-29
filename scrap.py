import urllib
from bs4 import BeautifulSoup
import requests
import re
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["travelbig1"]

mycol = mydb["big_col1"]

urls = ['https://www.keralatourism.org/destination/munnar/202',
        'https://www.keralatourism.org/destination/periyar-tiger-reserve-idukki/192',
        'https://www.keralatourism.org/destination/fort-kochi/422',
        'https://www.keralatourism.org/destination/alappuzha-beach/60',
        'https://www.keralatourism.org/destination/bekal-kasaragod/259',
        'https://www.keralatourism.org/destination/vagamon-idukki/324',
        'https://www.keralatourism.org/destination/muzhapilangad-beach/85',
        'https://www.holidify.com/state/kerala/',
        'https://www.makemytrip.com/holidays-india/kerala-tourism.html',
        'https://www.ekeralatourism.net/']
for url in urls:

    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data)
    links=[]
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    links = list(set(links))

    for link in links:
        #print(link.get('href'))
        if (link is not None) and ("www.keralatourism.org" in link or "www.makemytrip.com/holidays-india/kerala" in link or "www.holidify.com/pages/kerala" in link or "www.ekeralatourism.net" in link):
            r = requests.get(link)
            html_content = r.text

            soup = BeautifulSoup(html_content, 'html.parser')
            if soup.title:

                title = soup.title.string
            namebox = soup.find_all('p')
            if not namebox:
                continue
            text = ""
            for name in namebox[:4]:
                temp = name.text
                # temp.split()

                text = text + " " + temp
                # text.split()

            #  print("new")
            text = " ".join(text.split())

            mydict = {"url": url, "title": title, "text": text}

            x = mycol.insert_one(mydict)

