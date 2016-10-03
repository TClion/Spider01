"""这是抓取网易新闻主页当天热门新闻的爬虫，主要抓取新闻标题和链接"""

import requests
from lxml import etree


def getHtml(url):
    r = requests.get(url)
    return r.content


#解析出a节点下的内容，分析出新闻的url和title
def getInfo(Html):
    page = etree.HTML(Html)
    link = page.xpath(u'//a')       #内容在a节点下
    d = {}
    for i in link:
        if len(i.values()) == 1:    #只有1个字符串的才是正确的url
            url = i.values()[0]
            if '.html' in url:      #url都是html为结尾的字符串
                d[i.text] = url
    print(d)


if __name__ == '__main__':
    Url = "http://news.163.com/"    #网易新闻的主页
    Html = getHtml(Url)
    getInfo(Html)