"""这是抓取网易新闻主页当天热门新闻的爬虫，主要抓取新闻标题,链接和内容，并放在mysql wangyinews表中"""

import requests
from lxml import etree
import pymysql

#得到页面内容
def getHtml(url):
    html = requests.get(url)
    return html.text

#解析网页出标题和链接并返回一个字典
def getInfo(url):
    html = getHtml(url)
    page = etree.HTML(html)
    title = page.xpath('//li/a')
    d = {}
    for i in title:
        text = i.xpath('string(.)').replace(' ','').replace('\n','')
        if '.html' == i.attrib['href'][-5:] and text != '':
            d[text] = i.attrib['href']
    return d


#解析出相应页面的内容资讯
def gettext(url):
    html = getHtml(url)
    page = etree.HTML(html)
    text = page.xpath('string(//div[@class="post_text"])')
    return text.replace(' ','').replace('\n','')


#保存到mysql wangyinews中
def Save(d,db,cursor):
    for key,values in d.items():
        sql = """insert into wangyinews values (%s,%s,%s)"""
        data = (key,values,gettext(values))
        try:
            cursor.execute(sql,data)
        except Exception as e:
            print(e)
            db.rollback()



if __name__ == '__main__':
    Url = "http://news.163.com/"    #网易新闻的主页
    db = pymysql.connect('localhost','root','topcoder','p1_db',charset='utf8')  #连接数据库
    cursor = db.cursor()
    db.autocommit(True)
    d = getInfo(Url)
    Save(d,db,cursor)
    db.close()

