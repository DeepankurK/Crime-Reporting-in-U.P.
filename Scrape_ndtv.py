import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
import time 
import re
import pandas as pd
import sys
from csv import DictWriter
from datetime import datetime
import math
option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument("--disable-gpu")
option.add_argument("no-sandbox")
driver_path="/usr/bin/chromedriver"

columns=['City','Title','Text']
dic={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
d=int(sys.argv[1])
with open('NDTV.csv','a+') as file:
    #for p in range(day+1,31,1):
    for day in range(d,math.ceil(d/10)*10+1,1):
        #day=31
        print(day)
        writer_object = DictWriter(file,fieldnames=columns)
        num=int(sys.argv[2]) if len(sys.argv)==2 else 0
        driver = webdriver.Chrome(options=option, executable_path=driver_path)
        driver.get("https://archives.ndtv.com/articles/2019-01.html")
        print(driver.find_elements_by_id("ui-id-"+str(2*day-1))[0])
        driver.find_elements_by_id("ui-id-"+str(2*day-1))[0].click();
        soup_file=driver.page_source
        soup = BeautifulSoup(soup_file, 'html.parser')
        driver.close()
        time.sleep(1)
        driver.quit()  
        ls=soup.find_all(id="ui-id-"+str(2*day))
        temp=[]
        for i in str(ls[0]).split('\n'):
            if '<a href="' in i:
                link=i.split('"')[1]
                title=i.split('"')[2].split('<')[0].split('>')[1]
                fl=0
                for j in title:
                    if j >= 'z':
                        fl=1
                if fl==0: temp.append([title,link])
        print("CHANGE/: ",day,num,len(temp))
        for k in range(num,len(temp),1):
            link=temp[k][1]
            title=temp[k][0] 
            if '/science/' not in link and 'ndtv' in link and '/cricket/' not in link and '/bollywood/' not in link and '/bengali/' not in link and '/television/' not in link and '/moretogive/' not in link and'doctor.ndtv.com' not in link and '/indians-abroad/' not in link and 'swachhindia.ndtv.com' not in link and '/food/' not in link and '/offbeat/' not in link and '/zara-hatke/' not in link and '/business/' not in link and '/tennis/' not in link and '/education/' not in link and 'auto.ndtv.com' not in link and  'sports.ndtv.com' not in link and '/jobs/' not in link and 'gadgets.ndtv.com' not in link and 'swirlster.ndtv.com' not in link and '/entertainment/' not in link and 'food.ndtv.com' not in link and '/career/' not in link and '/health/' not in link:
                if '-news/' not  in link or ('/india-news/' in link and ('kanpur' in title or 'ghaziabad' in title or 'lucknow' in title or 'uttar ' in title.lower() or 'UP' in title)) or '/up-news/' in link or '/uttar-pradesh-news/' in link or '/kanpur-news/' in link or '/lucknow-news/' in link or '/ghaziabad-news/' in link:
                    print(day,k,link)
                    driver = webdriver.Chrome(options=option, executable_path=driver_path)
                    try:
                        driver.get(link)
                    except:
                        time.sleep(10)
                        driver.get(link)
                    soup_file2=driver.page_source
                    
                    soup = BeautifulSoup(soup_file2, 'html.parser')
                    
                    q=soup.find_all(class_="sp-descp")
                    if len(q)!=0:
                        a=str(q[0]).split('>')[1].split("<")[0]
                    else: a=""
                    txt=soup.find_all(id="ins_storybody")
                    txt=re.sub('<[^>]+>', '', str(txt[0].find_all('p')))
                    txt3=a+txt[1:-2]
                    if txt3=='':
                        print("ERROR ",day,num)
                    if 'kanpur' in txt3.lower() or 'kanpur' in title.lower():
                        writer_object.writerow({'City':'Kanpur','Title':title,'Text':txt3})
                        print('Kanpur')
                    if 'lucknow' in txt3.lower() or 'lucknow' in title.lower():
                        writer_object.writerow({'City':'Lucknow','Title':title,'Text':txt3})
                        print('Lucknow')
                    if 'ghaziabad' in txt3.lower() or 'ghaziabad' in title.lower():
                        writer_object.writerow({'City':'Ghaziabad','Title':title,'Text':txt3})
                        print('Ghaziabad')
                    #if 'UP' in txt3 or 'UP' in title:
                    #    writer_object.writerow({'City':'U.P.','Title':title,'Text':txt3})
                #elif 'uttar pradesh' in txt3.lower() or 'uttar pradesh' in title.lower():
                #    writer_object.writerow({'City':'U.P.','Title':title,'Text':txt3})
                #elif 'u.p.' in txt3.lower() or 'u.p.' in title.lower():
                #    writer_object.writerow({'City':'U.P.','Title':title,'Text':txt3})
                    driver.close()
                    time.sleep(1)
                    driver.quit()
        num=0
        #break
'''
driver = webdriver.Chrome(options=option, executable_path=driver_path)
driver.get("https://archives.ndtv.com/articles/2019-01.html")
el=driver.find_elements_by_id("ui-id-"+str(2*day-1))  
print(el,len(el))
'''