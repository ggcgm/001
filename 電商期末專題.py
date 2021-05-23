# -*- coding: utf-8 -*-
"""
Created on Thu May 20 06:25:06 2021

@author: USER
"""

from selenium import webdriver
from datetime import datetime
import csv
from bs4 import BeautifulSoup
import sys
from selenium.webdriver.support.ui import Select
import time
import pymysql
import re

search_list=[]
limit_list=[]
print("請輸入欲搜尋的商品關鍵字")
key=input()
print("請輸入商品價格的最大值")
max_price=input()
max_price=int(max_price)
print("請輸入商品價格的最小值")
min_price=input()
min_price=int(min_price)
search_day=datetime.now().strftime('%Y%m%d')


with open('四大商城爬蟲.csv','w+',newline='', encoding="utf-8-sig") as csvfile:   #解決多一空行 newline=''
    writer = csv.writer(csvfile)
    writer.writerow(('商品名','價格','網站','連結','關鍵字','搜尋時間'))
    
    
    
    url="https://www.momoshop.com.tw/main/Main.jsp"
    options=webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver=webdriver.Chrome(chrome_options=options)
    driver.get(url)
    driver.find_element_by_id("keyword").click()
    driver.find_element_by_id("keyword").clear()
    driver.find_element_by_id("keyword").send_keys(key)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    
    time.sleep(3)
    html = driver.page_source
    sp=BeautifulSoup(html,"html.parser")
    MOMO_name=sp.select("div.prdInfoWrap > h3")#商品名
    MOMO_price=sp.select("div.prdInfoWrap > p > span > b")#價格
    MOMO_url=sp.select("div.listArea > ul > li > a")
    print("[MOMO購物網]")
    for i in range(len(MOMO_name)):  
        print(i+1)
        print(MOMO_name[i].text,end=' ')
        print("[MOMO購物網]",end=' ')
        a=MOMO_price[i].text
        c=a.replace(',', '')
        print(MOMO_price[i].text,end=' ')
        print("https://www.momoshop.com.tw"+MOMO_url[i].get('href'))
        search_list.append([MOMO_name[i].text,c,"MOMO購物網","https://www.momoshop.com.tw"+MOMO_url[i].get('href'),key,search_day])
        
    print("[PChome線上購物]")
    url="https://shopping.pchome.com.tw/"
    driver.get(url)

    time.sleep(3)

    driver.get("https://shopping.pchome.com.tw/")
    driver.find_element_by_id("keyword").click()
    driver.find_element_by_id("keyword").clear()
    driver.find_element_by_id("keyword").send_keys(key)
    driver.find_element_by_id("doSearch").click()
    # driver.find_element_by_link_text(u"精準度").click()

    time.sleep(3)
    html = driver.page_source
    sp=BeautifulSoup(html,"html.parser")
    PChome_name=sp.select("div.Cm_C > dl > dd > h5 > a ")#商品名
    PChome_price=sp.select("div.Cm_C > dl > dd > ul > li > span > span")#價格
    PChome_url=sp.select("div.Cm_C > dl > dd > h5 > a ")#網址
        
    for i in range(len(PChome_name)):  
        print(i+1)
        print(PChome_name[i].text,end=' ')
        print("[PChome線上購物]",end=' ')
        print(PChome_price[i].text,end=' ')
        print("https:"+PChome_url[i].get('href'))
                
        search_list.append([PChome_name[i].text,PChome_price[i].text,"PChome線上購物","https:"+PChome_url[i].get('href'),key,search_day])
                
    print("[蝦皮商城]")
    url="https://shopee.tw/mall/search?keyword="+key
    driver.get(url)

    time.sleep(15)
    
    html = driver.page_source
    sp=BeautifulSoup(html,"html.parser")
    shopee_name=sp.select("div.yQmmFK")#商品名
    shopee_price=sp.find_all("div", class_="WTFwws _1lK1eK _5W0f35")#價格
    shopee_url=sp.select("div.col-xs-2-4 > a")#網址
        
    for i in range(len(shopee_name)):  
        print(i+1)
        print(shopee_name[i].text,end=' ')
        print("[蝦皮商城]",end=' ')
        a=shopee_price[i].text
        b=a.replace('$', '')
        c=b.replace(',', '')
        d=str(c).split( )[0]
        print(d)
        print("https://shopee.tw/" + shopee_url[i].get('href'))
        
        search_list.append([shopee_name[i].text,d,"蝦皮商城","https://shopee.tw/"+shopee_url[i].get('href'),key,search_day])
    print("[YAHOO超級商城]")
    
    
    url="https://tw.mall.yahoo.com/search/product?p="+key
    driver.get(url)
    # 100
    html = driver.page_source
    sp=BeautifulSoup(html,"html.parser")
    YAHOO_name=sp.find_all("span", class_="BaseGridItem__title___2HWui")#商品名
    YAHOO_price=sp.find_all("em")#價格
    YAHOO_url=sp.select("li.BaseGridItem__grid___2wuJ7 > a")
        
    for i in range(len(YAHOO_price)):  
        print(i+1)
        print(YAHOO_name[i].text,end=' ')
        print("[YAHOO超級商城]",end=' ')
        a=YAHOO_price[i].text
        b=a.replace('$', '')
        c=b.replace(',', '')
        print(YAHOO_price[i].text)
        print(YAHOO_url[i].get('href'))
        search_list.append([YAHOO_name[i].text,c,"YAHOO超級商城",YAHOO_url[i].get('href'),key,search_day])
    
    url="https://www.ruten.com.tw/find/?q="+key
    driver.get(url)
    html = driver.page_source
    sp=BeautifulSoup(html,"html.parser")
    ruten_name=sp.select("div.prod_info > h5 > a")#商品名
    ruten_price=sp.find_all("div", class_="price_box about")#價格


    for i in range(len(ruten_name)):  
        print(i+1)
        print(ruten_name[i].text,end=' ')
        print("[露天拍賣]",end=' ')
        x=ruten_name[i].text
        y=x.replace(',', '')
        a=ruten_price[i].text
        b=a.replace('$', '')
        c=b.replace(',', '')
        d=c.replace("約", '')
        e=str(d).split( )[0]
        e=int(e)
        print(e)
        print(ruten_name[i].get('href'))
        search_list.append([y,e,"露天拍賣網",ruten_name[i].get('href'),key,search_day])            

    for i in range(len(search_list)): 
        if int(search_list[i][1]) > min_price  and int(search_list[i][1]) < max_price :
            limit_list.append(search_list[i])   
            
    limit_list.sort(key=lambda s: int(s[1]))  
    
    for i in range(len(limit_list)): 
        writer.writerow([limit_list[i][0],limit_list[i][1],limit_list[i][2],limit_list[i][3],limit_list[i][4],limit_list[i][5]])
        
    driver.close()               #關閉瀏覽器
    

sys.exit

# db = pymysql.connect(host='163.15.24.35',port=3306,user='chenlw',passwd='abcd1234',db='mybooks',charset='utf8')              ####連線到 TQC_SRV031，記得改IP
# cursor = db.cursor()

# # with open('四大商城爬蟲.csv', "r", encoding="utf-8-sig") as fp2:
# with open('四大商城爬蟲.csv', "r", encoding="utf-8-sig") as fp2:    
#     message2=fp2.readlines()
#     # r2=fp2.read() 


# for k in range(2,len(message2),2):                      #正規化處裡，排除字串裡的,
#     while 1:
#         mm = re.search(",...元",message2[k])
#         if mm:
#             mm = mm.group()
#             message2[k] = message2[k].replace(mm,mm.replace(',',''))
#             print(message2[k])
#         else:
#             break

# # a="https://www.ettoday.net"
# # for i in range(3,len(message2),2):
# #     message2[i]=a+message2[i]
# #     message2[i-1]=message2[i-1]+','+message2[i]
# #     # print(a+i)

# f=limit_list
# for i in range(2,len(message2),2):
#     f.append(message2[i].split(','))
    
# cursor.execute('select name,price,website,link from shopping')
# data = cursor.fetchall()

# # for row in data:
# #     print(row[0], row[1], row[2], row[3])
#     #print(row)

# for j in range(len(f)):
    
#     # print(tuple(f[j][1:]) not in data)
#     if (tuple(f[j][1:]) not in data):              #新的才寫入
#         sql = '''insert into shopping (name,price,website,link)
#               values('{0}','{1}','{2}','{3}')'''
#         sql = sql.format(f[j][0],f[j][1],f[j][2],f[j][3])
#         # print(f[j])
#         cursor.execute(sql)
#         db.commit()


# db.close()