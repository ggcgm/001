# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 19:43:21 2020

@author: USER
"""

from selenium import webdriver
import csv
from bs4 import BeautifulSoup
import time,datetime
import sys
from selenium.webdriver.support.ui import Select

key="iphone12mini64g"
url="https://shopping.pchome.com.tw/"
options=webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
driver=webdriver.Chrome(chrome_options=options)
driver.get(url)

time.sleep(3)

driver.get("https://shopping.pchome.com.tw/")
driver.find_element_by_id("keyword").click()
driver.find_element_by_id("keyword").clear()
driver.find_element_by_id("keyword").send_keys(key)
driver.find_element_by_id("doSearch").click()
driver.find_element_by_link_text(u"精準度").click()

time.sleep(10)

with open('PChome爬蟲.csv','w+',newline='', encoding="utf-8-sig") as csvfile:   #解決多一空行 newline=''
    writer = csv.writer(csvfile)
    writer.writerow(('商品名','網站','價格','連結'))
    
    


    html = driver.page_source
    sp=BeautifulSoup(html,"html.parser")
    search_name=sp.select("div.Cm_C > dl > dd > h5 > a ")#商品名
    search_price=sp.select("div.Cm_C > dl > dd > ul > li > span > span")#價格
    search_url=sp.select("div.Cm_C > dl > dd > h5 > a ")#網址
        
    for i in range(len(search_name)):  
        print(i+1)
        print(search_name[i].text,end=' ')
        print("[PChome線上購物]",end=' ')
        print(search_price[i].text,end=' ')
        print("https:"+search_url[i].get('href'))
                
            
        writer.writerow([search_name[i].text,"PChome線上購物",search_price[i].text,"https:"+search_url[i].get('href')])
                
driver.close()               #關閉瀏覽器


sys.exit             