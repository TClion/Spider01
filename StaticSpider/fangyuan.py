"""测试正则表达式和xpath的性能，下载房源信息，价格，链接，和房源地址。
   url是安居客的顺义城区二手房链接，如何要抓取其他如出租房等信息需大改，提前在mysql数据库中创建fangyuan表。"""

import requests
from lxml import etree
import timeit
import re
import time
import pymysql


url = "http://beijing.anjuke.com/sale/shunyicheng/p"        #安居客二手房
S = requests.Session()

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Host':'beijing.anjuke.com',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
}

#用相对路径查找，比绝对路径要慢，循环是每次抓取不同的页面
def Xpath01():
    for i in range(1,10):
        time.sleep(0.5)
        Url = url+str(i)
        r = S.get(Url,headers=header)
        c = r.content
        page = etree.HTML(c)
        title = page.xpath('//div[@class="house-title"]/a')
        Title = [i.attrib['title'] for i in title]
        info = page.xpath('//div[@class="details-item"]')
        Info = [i.xpath('string(.)').replace('\n','').replace(' ','') for i in info]
        address = page.xpath('//span[@class="comm-address"]')
        Address = [i.attrib['title'] for i in address]
        money = page.xpath('//strong')
        Money = [i.text+'万' for i in money]
        href = page.xpath('//div[@class="house-title"]/a')
        Href = [i.attrib['href'] for i in href]

#相对路径
def Xpath02():
    for i in range(1,40):
        time.sleep(0.2)
        Url = url+str(i)
        r = S.get(Url,headers=header)
        c = r.content
        page = etree.HTML(c)
        title = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[2]/div[1]/a')
        Title = [i.attrib['title'] for i in title]
        address = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[2]/div[3]/span')
        Address = [i.attrib['title'].replace('\xa0\xa0',' ') for i in address]
        money = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[3]/span/strong')
        Money = [i.text+'万' for i in money]
        href = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[2]/div[1]/a')
        Href = [i.attrib['href'] for i in href]
        info = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[2]/div[2]')
        Info = [i.xpath('string(.)').replace('\n','').replace(' ','') for i in info]


#解析网页并保存到fangyuan数据库中
def Xpath04():
    db = pymysql.connect('localhost','root','topcoder','p1_db',charset='utf8')  #数据库连接，charset必需
    db.autocommit(True)         #保持持续提交
    cursor = db.cursor()
    sql = """delete from fangyuan"""            #先删除表中原来的数据
    cursor.execute(sql)
    for i in range(1,2):                        #实现翻页的功能，只能前50页
        time.sleep(0.2)
        Url = url+str(i)
        r = S.get(Url,headers=header)
        c = r.content
        page = etree.HTML(c)
        title = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[2]/div[1]/a/@title')
        address = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[2]/div[3]/span')
        Address = [i.attrib['title'].replace('\xa0\xa0',' ') for i in address]
        money = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[3]/span/strong')
        Money = [i.xpath('string(.)').strip()+'万' for i in money]
        href = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[2]/div[1]/a/@href')
        info = page.xpath('/html/body/div[1]/div[2]/div[5]/ul/li/div[2]/div[2]')
        Info = [i.xpath('string(.)').strip()for i in info]
        L = list(zip(title,Address,Money,href,Info))
        for title,address,money,href,info in L:
            sql = """insert into fangyuan values (%s,%s,%s,%s,%s)"""
            data = (address,money,href,info,title)
            try:
                cursor.execute(sql,data)
            except  Exception as e:
                print(e)
                db.rollback()
    db.close()


#数据库查询
def Print():
    db = pymysql.connect('localhost','root','topcoder','p1_db',port=3306,charset='utf8')
    cursor = db.cursor()
    sql = """select * from fangyuan"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print(row[0],row[1],row[2],row[3],row[4])
    except:
        print('error')
    db.close()



#正则表达式分析页面，问题多，比xpath慢
def Re():
    for i in range(1,40):
        time.sleep(0.5)
        Url = url+str(i)
        r = S.get(Url,headers=header)
        text = r.text
        t = re.compile(r'<a data-from.+title="(.+?)"')
        titles = t.findall(text)
        h = re.compile(r'href="(http://beijing.+\?.+&.+)"')
        href = h.findall(text)
        a = re.compile(r'title=".+\[(.+)\]"')
        address = a.findall(text)
        m = re.compile(r'<strong>(\d+)</strong>\b')
        money = m.findall(text)
        i =re.compile(r'<span>([\w|\s]+)</span><em>')  #bug
        info = i.findall(text)








if __name__ == '__main__':
    Xpath04()
    Print()

    """
    print(timeit.timeit("Xpath01()","from __main__ import Xpath01",number=1))
    print(timeit.timeit("Xpath02()","from __main__ import Xpath02",number=1))
    print(timeit.timeit("Xpath04()","from __main__ import Xpath04",number=1))
    print(timeit.timeit("Re()","from __main__ import Re",number=1))
    """


