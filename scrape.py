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
option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument("--disable-gpu")
option.add_argument("no-sandbox")
driver_path="/usr/bin/chromedriver"

columns=['City','Title','Text']
dic={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
base=43466
mon=int(sys.argv[1])

with open('Month_'+str(mon)+'.csv','a+') as file:
    for p in range(1,mon,1):
        base=base+dic[p]
    print(base)
    writer_object = DictWriter(file,fieldnames=columns)
    num=int(sys.argv[3]) if len(sys.argv)==4 else 0
    for d in range(int(sys.argv[2])-1,dic[mon],1):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        driver = webdriver.Chrome(options=option, executable_path=driver_path)
        driver.get("https://timesofindia.indiatimes.com/2019/"+str(mon)+"/"+str(d+1)+"/archivelist/year-2019,month-"+str(mon)+",starttime-"+str(base+d)+".cms")
            #driver.get("https://timesofindia.indiatimes.com/2019/"+str(mon)+"/"+str(d+1)+"/archivelist/year-2019,month-"+str(mon)+",starttime-"+str(base+d)+".cms")
        soup_file=driver.page_source
        soup = BeautifulSoup(soup_file, 'html.parser')
        table=soup.find_all('table', class_='cnt')
        cont=table[1].find_all('table')
        ls=cont[0].find_all('a')
        driver.close()
        time.sleep(1)
        driver.quit()  
        print("CHANGE: ",mon,d+1,len(ls))
        for k in range(num,len(ls),1):
            i=ls[k]
            link=i.get('href')
            title=re.sub('<[^>]+>', '', str(i)) 
            if 'timesofindia' in link and '/entertainment' not in link and '/world/' not in link and '/tv/news' not in link and '/news/kannada' not in link and '/citizen-reporter' not in link and '/news/bengali' not in link and '/auto/' not in link and '/home/environment/' not in link and '/astrology/' not in link and '/news/marathi' not in link and '/news/tamil' not in link  and 'most-searched-products' not in link and '/companies/' not in link and '/best-products/' not in link and '/gadgets-news/' not in link and '/home/education' not in link and 'spirituality' not in link and '/life-style' not in link and '/gaming' not in link and '/science' not in link and '/business' not in link and '//sports' not in link:
                if '//city/' in link and '//city/kanpur' not in link and '//city/lucknow' not in link and '//city/ghaziabad' not in link:
                    continue
                if '//elections' in link and '/up/news' not in link and '/india/news' not in link:
                    continue
                print(d+1,k,link)
                driver = webdriver.Chrome(options=option, executable_path=driver_path)
                try:
                    driver.get(link)
                except:
                    time.sleep(10)
                    driver.get(link)
                soup_file2=driver.page_source
                soup = BeautifulSoup(soup_file2, 'html.parser')
                if len(soup.find_all(class_="ga-headlines"))!=0:
                    txt=soup.find_all(class_="ga-headlines")[0]
                elif len(soup.find_all(class_="Normal"))!=0:
                    txt=soup.find_all(class_="Normal")[0]
                else:
                    continue
                    #print("ERROR:" +str(k)+" "+str(link)+str(" ")+str(title))
                txt2=re.sub('<[^>]+>', '', str(txt))
                txt3=re.sub('\n+', ' ', str(txt2))
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
        num=0#
#5 1 279
#1 1 383
#after 500 add sleep cluase
#4 7 390