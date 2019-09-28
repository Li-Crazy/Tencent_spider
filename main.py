'''
-*- coding: utf-8 -*-
@Author  : LiZhichao
@Time    : 2019/4/16 20:46
@Software: PyCharm
@File    : main.py
'''
from lxml import etree
import requests

BASE_DOMAIN = "https://hr.tencent.com/"
HEADERS = {
    # "Referer": "https://hr.tencent.com/position.php?keywords=python&start=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ("
                  "KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 "
                  "Core/1.70.3650.400 QQBrowser/10.4.3341.400"
}

def get_datail_url(url):
    response = requests.get(url,headers=HEADERS)
    text = response.text
    # parser = etree.HTMLParser('utf-8')
    # print(text)
    html = etree.HTML(text)
    detail_urls = html.xpath("//td[@class='l square']//a/@href")
    detail_urls = map(lambda url: BASE_DOMAIN + url, detail_urls)
    # for detail_url in detail_urls:
    #     detail_url = BASE_DOMAIN+detail_url
    #     break

    return detail_urls
        # print(detail_url)

def  detail_page(url):
    response = requests.get(url, headers=HEADERS)
    text = response.text
    # print(text)
    # parser = etree.HTMLParser('utf-8')
    html = etree.HTML(text)
    position = {}
    title = html.xpath("//tr[@class='h']//td/text()")[0]
    position['title'] = title
    infos = html.xpath("//tr[@class='c bottomline']//td")
    for info in infos:
        info1 = info.xpath(".//span/text()")[0]
        info2 = info.xpath("./text()")[0]
        position[info1] = info2
        # print(etree.tostring(info,encoding='utf-8').decode('utf-8'))
        # print(info1)
        # print(info2)
    requires = html.xpath("//td[@class='l2']")
    for require in requires:
        # print(etree.tostring(require, encoding='utf-8').decode('utf-8'))
        claims = require.xpath("./div[@class='lightblue']/text()")
        for claim in claims:
            # print(claim)
            specific = require.xpath("./ul[@class='squareli']//li/text()")
            position[claim]=specific
            # print(specific)
            return position
def spider():
    base_url = "https://hr.tencent.com/position.php?keywords=python&start={}#a"
    tencent_position = []
    for i in range(0, 57):
        x = 10 * i
        url = base_url.format(x)
        detail_urls = get_datail_url(url)
        for detail_url in detail_urls:

            print(detail_url)
            position = detail_page(detail_url)
            tencent_position.append(position)
            print(position)
    print(tencent_position)


if __name__ == '__main__':
    spider()
