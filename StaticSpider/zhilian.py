"""这是一个抓取智联招聘信息的爬虫，职位和工作地点由用户输入，结果放在职位清单.xlsx中"""

import requests
from lxml import etree
from openpyxl import Workbook
import urllib
from urllib import parse as urllib


wb = Workbook()
filename = "职位清单.xlsx"
ws1 = wb.active
ws1.title = "结果"
Url = "http://sou.zhaopin.com/jobs/searchresult.ashx?"


#返回目标页面的byte类型
def getHtml(url):
    r = requests.get(url)
    return r.content


#解析出公司，职位，月薪，更新日期和简介
def getInfo(Html, number):
    page = etree.HTML(Html.decode('utf-8'))
    company = page.xpath(u'//table/tr/td[@class="gsmc"]/a')
    position = page.xpath(u'//td[@class="zwmc"]/div')
    money = page.xpath(u'//td[@class="zwyx"]')
    data = page.xpath(u'//td[@class="gxsj"]/span')
    text = page.xpath(u'//div[@class="clearfix"]/ul')
    companys = [i.text for i in company if i.text!=None]
    positions = [i.xpath('string(.)').strip() for i in position]
    moneys = [i.text for i in money]
    datas = [i.text for i in data]
    texts = [i.xpath('string(.)').strip() for i in text]
    L = list(zip(companys,positions,moneys,datas,texts))
    n = number+len(L)
    for company,position,money,data,text in L:  #将内容依次放入execl文件中
        col_A = 'A%s'%(number)
        col_B = 'B%s'%(number)
        col_C = 'C%s'%(number)
        col_D = 'D%s'%(number)
        col_E = 'E%s'%(number)
        ws1[col_A] = company
        ws1[col_B] = position
        ws1[col_C] = money
        ws1[col_D] = data
        ws1[col_E] = text
        number += 1
    wb.save(filename=filename)
    return n                        #更新标记位


if __name__ == '__main__':
    print("智联招聘查找，默认前10页")
    place = input("请输入要查询的地区:")
    position = input("请输入你要找的职位:")
    name = urllib.quote(place)          #将地区变为url可识别的编码
    zw = urllib.quote(position)         #将职位变为url可识别的编码
    Url += 'jl=%s&kw=%s&p=1' %(name,zw)         #更新url
    n = 1
    for i in range(1,11):
        Url = Url[:-1] + str(i)                 #改变url的页数
        Html = getHtml(Url)
        n = getInfo(Html,n)             #保持标记位的更新，主要用于execl表格
    print("您要查寻的结果已保存在职位清单.xlsx中")