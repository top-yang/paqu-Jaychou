from selenium import webdriver
import selenium.webdriver.support.ui as ui
import os
from bs4 import BeautifulSoup
import requests
import time
def get_html_text(page):
    soup=BeautifulSoup(str(page),'html')
def write2txt(data,path):
    try:
        file = open(path,"w",encoding='utf-8')
        file.write(data)
        file.close()
    except:
        print('失败\n')
def get_content(url):
    #data=''
    time.sleep(3)
    filename=time.strftime('%Y-%m-%d-%H-%M-%S')+'.txt'
    try:
        r=requests.get(url)
        #print(r.request.url)
        r.encoding=r.apparent_encoding
        r.raise_for_status()
        write2txt(r.text,'C:/Users/Jay1chou/AppData/Local/Programs/Python/Python36/spider_data/'+filename)
    except:
        print("爬取失败"+url+'\n')
def gethref(word,pn):
    data=''
    driver = webdriver.Firefox(executable_path="C:/Program Files (x86)/Mozilla Firefox/geckodriver.exe")
    driver.get("http://www.baidu.com/s?wd="+word+"&pn="+pn+"&tn=baidurt&ie=utf-8&rtt=4&bsst=1")
    try:
        wait = ui.WebDriverWait(driver, 15)
        if wait.until(lambda driver: driver.find_element_by_class_name('content_bg')):
            lists = driver.find_element_by_class_name('content').find_elements_by_tag_name('table')
            #print(len(lists))
            for i in lists:
               istr=i.find_elements_by_tag_name('a')[0].get_attribute('href')
               get_content(istr)#爬取前20个网页
               data+=istr+'\n'
        return data
    finally:
        driver.quit()
data=''
word='周杰伦'
pn='0'
data1=gethref(word,pn)
pn='10'
data2=gethref(word,pn)
data=data1+data2
# 存储为文本
filename=time.strftime('%Y-%m-%d')+'.txt'
write2txt(data,'C:/Users/Jay1chou/AppData/Local/Programs/Python/Python36/url_daily/'+filename)#保存每天爬的文件
#getLyrics()
