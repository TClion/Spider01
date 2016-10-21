"""抓取天涯主页帖子的标题，分类，和网页链接，并放在mysql中。以后会添加更多功能"""
import requests
from lxml import etree
import pymysql

#获得天涯主页的html
def gethtml(url):
    r = requests.get(url)
    text = r.text
    page = etree.HTML(text)
    return page


#用xpath解析
def getInfo(page):
    title = page.xpath('//li/span/a/text()')
    info  = page.xpath('//li/div/a/text()')
    href = page.xpath('//li/div/a/@href')
    L =list(zip(title,info,href))
    return L

#保存在数据库表tianya中
def Save(L,db,cursor):
    for title,info,href in L:
        sql = """insert into tianya values(%s,%s,%s)"""
        data = (title,info,href)
        try:
            cursor.execute(sql,data)
        except Exception as e:
            print(e)
            db.rollback()


if __name__ == '__main__':
    db = pymysql.connect('localhost','root','topcoder','p1_db',charset='utf8')  #链接数据库
    cursor = db.cursor()
    db.autocommit(True)
    url = "http://bbs.tianya.cn/"
    page = gethtml(url)
    L = getInfo(page)
    Save(L,db,cursor)
    db.close()
