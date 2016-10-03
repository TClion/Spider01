"""豆瓣电影top250爬虫程序，能抓取豆瓣电影top250每个电影的名称，
   评分和评价人数，并存放在电影.xlsx中
"""
import requests
from lxml import etree
from openpyxl import workbook
from openpyxl import Workbook

#创建execl文件
db = Workbook()
filename = "电影.xlsx"
db1 = db.active
db1.title = "电影top250"


def getHtml(url):
    Html = requests.get(url)
    return Html.content


def getInfo(Html,number):
    page = etree.HTML(Html)
    names = page.xpath(u'//img[@class=""]')
    scores = page.xpath(u'//span[@class="rating_num"]')
    numbers = page.xpath(u'//div[@class="star"]/span[4]')
    #jianjie = page.xpath(u'//span[@class="inq"]')          #由于有的电影没有简介，先不抓取，以后补上功能
    Names = [i.attrib["alt"] for i in names]
    Scores = [i.text for i in scores]
    Numbers = [n.text for n in numbers]
    #Texts = [i.text for i in jianjie]
    MovieList = list(zip(Names,Scores,Numbers))
    n = number + len(MovieList)
    for Name,Score,Number in MovieList:
        col_A = 'A%s'%(number)
        col_B = 'B%s'%(number)
        col_C = 'C%s'%(number)
        db1[col_A] = Name
        db1[col_B] = Score
        db1[col_C] = Number
        number += 1
    db.save(filename=filename)
    return n                #返回标志位


if __name__=='__main__':
    n = 1
    for i in range(0,250,25):
        url = "https://movie.douban.com/top250"
        url = url+'?start='+str(i)              #实现翻页功能
        Html =getHtml(url)
        n = getInfo(Html,n)
