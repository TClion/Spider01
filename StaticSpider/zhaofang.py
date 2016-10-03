"""找房网爬虫，主要抓取北京海淀区出租的房子(前10页)，包含地址，链接和房屋介绍。
   数据很杂，以后会添加更多功能。
"""

import requests
from lxml import etree
import re


def GetHtml(url):
    r = requests.get(url)
    return r.content


def Getinfo(Html):
    info = etree.HTML(Html)
    link = info.xpath(u'//dl[@class="list hiddenMap rel"]/dt/a')
    names = info.xpath(u'//dl[@class="list hiddenMap rel"]/dd/p/a[@title]')
    text = info.xpath(u'//dl[@class="list hiddenMap rel"]/dd[@class="info rel"]')
    Links = ["http://zu.fang.com"+i.values()[1] for i in link]
    Names = [i.values()[2] for i in names]
    p = re.compile('\s+')           #抓取多个信息并去掉空格，以后会修改
    Text = [re.sub(p,'',i.xpath('string(.)')) for i in text]
    HomeList = list(zip(Names,Links,Text))
    for name,url,text in HomeList:
        print(name,url,text)


if __name__ == '__main__':
    url = "http://zu.fang.com/house-a00/i31"    #链接是固定的，缺乏灵活性
    for i in range(1,11):
        url = url[:-1] +str(i)
        Html = GetHtml(url)
        Getinfo(Html)
