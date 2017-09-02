"""这是一个抓取智联招聘信息的爬虫，职位和工作地点由用户输入，结果放在mysql zhilian表中,要提前建好zhilian表"""

import requests
from lxml import etree
import pymysql
from urllib import parse as urllib

Url = "http://sou.zhaopin.com/jobs/searchresult.ashx?"      #源链接

header = {

    'Host': 'sou.zhaopin.com',
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Connection': "keep-alive",

}

#解析出公司，职位，月薪，更新日期和简介
def getInfo(url):
    html = requests.get(url,headers=header)
    text = html.text
    page = etree.HTML(text)
    name = page.xpath('//td[@class="gsmc"]/a/text()')
    updatetime = page.xpath('//td[@class="gxsj"]/span/text()')
    info = page.xpath('//ul/li[@class="newlist_deatil_two"]')
    Info = [x.xpath('string(.)') for x in info]
    detail = page.xpath('//ul/li[@class="newlist_deatil_last"]')
    Detail = [x.xpath('string(.)') for x in detail]
    L = list(zip(name,Info,Detail,updatetime))
    return L


#保存在mysql zhilian表中
def SaveInfo(List,db,cursor):
    for name,info,detail,time in List:
        sql = """insert into zhilian values (%s,%s,%s,%s)"""
        data = (name,info,detail,time)
        try:
            cursor.execute(sql,data)
        except Exception as e:
            print(e)
            db.rollback()

if __name__ == '__main__':
    db = pymysql.connect('localhost','root','topcoder','p1_db',charset='utf8')  #连接数据库
    cursor = db.cursor()
    db.autocommit(True)
    print("智联招聘查找，默认前10页")
    place = input("请输入要查询的地区:")
    position = input("请输入你要找的职位:")
    name = urllib.quote(place)          #将地区变为url可识别的编码
    zw = urllib.quote(position)         #将职位变为url可识别的编码
    Url += 'jl=%s&kw=%s&p=1' %(name,zw)         #更新url
    for i in range(1,11):
        Url = Url[:-1] + str(i)                 #改变url的页数
        info = getInfo(Url)
        SaveInfo(info,db,cursor)
    db.close()
