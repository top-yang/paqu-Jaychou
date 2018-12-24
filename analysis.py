import requests
import os
import operator
import jieba
import jieba.analyse
import re
import chardet
import glob
from collections import Counter
from bs4 import BeautifulSoup
def printcount(slist):
    number=0
    char=''
    c=Counter()
    i=1
    for x in slist: 
        if len(x)>1:
            c[x]+=1
   # print("统计结果:")
    for (k,v) in c.most_common(100):
        if v>number:
            if k!='周杰伦':
                char=''.join(k)
                number=v
        i+=1
        if i>10:
            break
    return char,number
def get_html_txt(filename):
    file = open(filename,encoding='utf-8')
    file_txt=file.read()
    #file_txt.encoding = 'utf-8'
    soup = BeautifulSoup(file_txt, 'html.parser')
    part = soup.select('div')
    return part
def countchn(string):
    #pattern = re.compile(u'[\u1100-\uFFFDh]+?')
    pattern = re.compile(u'[\u4E00-\u9FA5]+?')
    result = pattern.findall(string)
    chnnum = len(result)            #list的长度即是中文的字数
    possible = chnnum/len(str(string))         #possible = 中文字数/总字数
    return (chnnum, possible)
def findtext(part):    
    length = 50000000
    l = []
    for paragraph in part:
        chnstatus = countchn(str(paragraph))
        possible = chnstatus[1]
        if possible > 0.15:         
            l.append(paragraph)
    l_t = l[:]
    #这里需要复制一下表，在新表中再次筛选，要不然会出问题，跟Python的内存机制有关
    for elements in l_t:
        chnstatus = countchn(str(elements))
        chnnum2 = chnstatus[0]
        if chnnum2 < 10:    
        #最终测试结果表明300字是一个比较靠谱的标准，低于300字的正文咱也不想要了对不
            l.remove(elements)
        else:
            length = len(str(elements))
            paragraph_f = elements
            return paragraph_f.text
if __name__ =='__main__':
    path='C:/Users/Jay1chou/AppData/Local/Programs/Python/Python36/spider_data/'
    fdir=os.listdir(path)
    k=''
    v=0
    d={}
    for name in glob.glob(os.path.dirname(path)+'/2018-05-16*'):
        flag=0
        print (name)
        part=get_html_txt(name)
        content1=str(part)
        content=re.sub("[\s+\.《》\“\”\!\/_,$%^*:：(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "",content1)
        pn=re.compile(u'[\u4E00-\u9FA5]+?')
        result=pn.findall(content)
        txt="".join(result)#.decode('utf-8')#列表转字符串
        jieba.load_userdict("userdict.txt")
        seg_list=" ".join(jieba.cut(txt))
        split_seg_list =seg_list.split()
        #print(split_seg_list)
        (k1,v1)=printcount(split_seg_list)
        print("热点词:%s 频度:%d"%(k1,v1))
        for mk in d.keys():
                #print(mk)
                if(mk==k1):
                    d[mk]+=v1
                    flag=1
                    break
        if flag==0:
            d[k1]=v1
        
    for mk,mv in d.items():
                if(mv>v):
                    v=mv
                    k=''.join(mk)
    print(d)
    print("当天最热点:%s 频度:%d"%(k,v))
