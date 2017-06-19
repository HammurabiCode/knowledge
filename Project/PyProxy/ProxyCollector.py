# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：    ProxyCollector.py
   Description :  抓取免费代理
   Author :       Hammurabi
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
-------------------------------------------------
"""
import re
import requests
from importlib import reload 
import sys
import platform
import time
from multiprocessing import Process
import ProxyDB
# sys.path.append('../')


def getHTMLText(url, headers={'user': 'Mozilla/5.0'}):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return response.status_code


def getHtmlTree(url, **kwargs):
    """
    获取html树
    :param url:
    :param kwargs:
    :return:
    """
    import requests
    from lxml import etree
    header = {'Connection': 'keep-alive',
              'Cache-Control': 'max-age=0',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate, sdch',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              }
    # TODO 取代理服务器用代理服务器访问
    html = requests.get(url=url, headers=header, timeout=30).content
    return etree.HTML(html)


def verifyProxy(proxy):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    import re
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    return True if re.findall(verify_regex, proxy) else False


# noinspection PyPep8Naming
def robustCrawl(func):
    def decorate(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.info(u"sorry, 抓取出错。错误原因:")
            logger.info(e)
    return decorate


# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()


HEADER = {'Connection': 'keep-alive',
          'Cache-Control': 'max-age=0',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          }


def get_360_proxy():
    proxy_list = []
    url = '''http://www.proxy360.cn/Proxy'''
    for div in get_page(url).find_all('div', 'proxylistitem'):
        span_list = div.find_all('span', 'tbBottomLine')
        if len(span_list) > 2:
                proxy = {
                    'addr': 'http://%s:%s' % (span_list[0].string.strip(' \r\n'), span_list[1].string.strip(' \r\n'))
                    , 'src': 'proxy360'
                }
                proxy_list.append(proxy)
    return proxy_list


def get_xici_proxy():
    # 西刺 高匿
    proxy_list = []
    for iPage in range(1, 11):
        proxy_on_page = []
        url = '''http://www.xicidaili.com/nn/%d''' % iPage
        tr_list = []
        try:
            tr_list = get_page(url).find_all('tr') 
            time.sleep(3)
        except Exception as e:
            logger.error(e)

        for tr in tr_list:
            td_list = tr.find_all('td')
            if len(td_list) > 2:
                proxy = {
                    'addr': 'http://%s:%s' % (td_list[1].string, td_list[2].string)
                    , 'src': '西刺'
                }
                proxy_on_page.append(proxy)
        logger.info('%d proxies on page %s' % (len(proxy_on_page), url))
        proxy_list.extend(proxy_on_page)
    return proxy_list


def get_kuai_proxy():
    proxy_list = []
    for iPage in range(1, 11):
        proxy_on_page = []
        url = '''http://www.kuaidaili.com/free/inha/%d/''' % iPage
        tr_list = []
        try:
            tr_list = get_page(url).find_all('tr') 
            time.sleep(3)
        except Exception as e:
            logger.error(e)

        for tr in tr_list:
            td_list = tr.find_all('td')
            if len(td_list) > 1:
                proxy = {
                    'addr': 'http://%s:%s' % (td_list[0].string, td_list[1].string)
                    , 'src': '快代理'
                }
                proxy_on_page.append(proxy)
        logger.info('%d proxies on page %s' % (len(proxy_on_page), url))
        proxy_list.extend(proxy_on_page)
    return proxy_list

class GetFreeProxy(object):
    """
    proxy getter
    """

    def __init__(self):
        pass

    @staticmethod
    @robustCrawl    #decoration print error if exception happen
    def freeProxyFirst(page=10):
        """
        抓取快代理IP http://www.kuaidaili.com/
        :param page: 翻页数
        :return:
        """
        url_list = ('http://www.kuaidaili.com/proxylist/{page}/'.format(page=page) for page in range(1, page + 1))
        # 页数不用太多， 后面的全是历史IP， 可用性不高

        for url in url_list:
            tree = getHtmlTree(url)
            proxy_list = tree.xpath('.//div[@id="index_free_list"]//tbody/tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    @staticmethod
    @robustCrawl
    def freeProxySecond(proxy_number=100):
        """
        抓取代理66 http://www.66ip.cn/
        :param proxy_number: 代理数量
        :return:
        """
        url = "http://m.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            proxy_number)

        html = getHTMLText(url, headers=HEADER)
        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy

    @staticmethod
    @robustCrawl
    def freeProxyThird(days=1):
        """
        抓取有代理 http://www.youdaili.net/Daili/http/
        :param days:
        :return:
        """
        url = "http://www.youdaili.net/Daili/http/"
        tree = getHtmlTree(url)
        page_url_list = tree.xpath('.//div[@class="chunlist"]/ul/li/p/a/@href')[0:days]
        for page_url in page_url_list:
            html = requests.get(page_url, headers=HEADER).content
            html=html.decode('utf-8')
            # print html
            proxy_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)
            for proxy in proxy_list:
                yield proxy

    @staticmethod
    @robustCrawl
    def freeProxyFourth():
        """
        抓取西刺代理 http://api.xicidaili.com/free2016.txt
        :return:
        """
        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    ]
        for each_url in url_list:
            tree = getHtmlTree(each_url)
            proxy_list = tree.xpath('.//table[@id="ip_list"]//tr')
            for proxy in proxy_list:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])

    @staticmethod
    @robustCrawl
    def freeProxyFifth():
        """
        抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
        这个不能用……
        :return:
        """
        url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
        for page in range(1, 10):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)
            proxy_list = tree.xpath('//td[@class="ip"]')
            for each_proxy in proxy_list:
                yield ''.join(each_proxy.xpath('.//text()'))

def collect():
    db = ProxyDB.ProxyDB()
    cnt = 0
    if db.lockForWrite():
        db.clear()
        gg = GetFreeProxy()
        l = [gg.freeProxyFirst, gg.freeProxySecond, gg.freeProxyThird, gg.freeProxyFourth]
        for f in l:
            for ip in f():
                if verifyProxy(ip):
                    db.add(ip)
                    cnt = cnt + 1
            print(cnt)
        db.unlock()
        print(cnt)
    else:
        print('locked')
    return cnt

def run():
    if platform.system() == 'Windows':
        print('Windows')
        collect()
    else:
        p1 = Process(target=collect, name='collect')
        p1.start()

if __name__ == '__main__':
    run()
