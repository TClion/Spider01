"""豆瓣电影top250爬虫程序，能抓取豆瓣电影top250每个电影的名称，导演和主演名称,评分和评价人数和简介.
   并存放在mysql中，提前在mysql数据库中创建doubanmovie表。
"""

import requests
from lxml import etree
import pymysql

#利用xpath解析网页
def GetInfo(url):
    html = requests.get(url)
    text = html.content
    page = etree.HTML(text)
    title = page.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[1]/a/img/@alt')
    score = page.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')
    number = page.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[4]/text()')
    info = page.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li/div/div[2]/div[2]/p[1]')
    Info = [i.xpath('string(.)').strip().replace('\xa0\xa0\xa0',' ').replace('\xa0/\xa0','|').replace(' ','').replace('...\n','  ') for i in info]
    Inq = []
    for i in range(1,26):
        X = '/html/body/div[3]/div[1]/div/div[1]/ol/li[%s]/div/div[2]/div[2]/p[2]/span/text()'% str(i)
        inq = page.xpath(X)
        if inq == []:
            Inq.append('NULL')
        else:
            Inq.append(inq[0])
    L = list(zip(title,Info,score,number,Inq))
    return L

#存放在mysql数据库doubanmovie中
def SaveInfo(L,db,cursor):
    for title,info,score,num,inq in L:
        sql = """insert into doubanmovie values (%s,%s,%s,%s,%s)"""
        data = (title,info,score,num,inq)
        try:
            cursor.execute(sql,data)
        except Exception as e:
            print(e)
            db.rollback()


if __name__ =='__main__':
    db = pymysql.connect('localhost','root','topcoder','p1_db',port=3306,charset='utf8')    #本地数据库,登录名,密码,要连接的数据库
    cursor = db.cursor()
    db.autocommit(True)
    sql = """delete from doubanmovie"""         #先删除表中数据
    cursor.execute(sql)
    url = "https://movie.douban.com/top250?start="      #实现翻页的功能
    for i in range(0,250,25):
        Url = url+str(i)
        info = GetInfo(Url)
        SaveInfo(info,db,cursor)
    db.close()



