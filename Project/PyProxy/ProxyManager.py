# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py  
   Description :  
   Author :       Hammurabi
   date：          
-------------------------------------------------
   Change Activity:
-------------------------------------------------
"""
__author__ = 'Hammurabi'

import redis
import ProxyDB
import ProxyCollector


class ProxyManager(object):
    """
    ProxyManager
    """

    def __init__(self):
        self.db = ProxyDB.ProxyDB()
        # self.config = GetConfig()
        # self.raw_proxy_queue = 'raw_proxy'
        # self.log = LogHandler('proxy_manager')
        # self.useful_proxy_queue = 'useful_proxy'
        pass

    def refresh(self):
        """
        fetch proxy into Db by ProxyGetter
        :return:
        """
        ProxyCollector.run()
        # for proxyGetter in self.config.proxy_getter_functions:
        #     proxy_set = set()
        #     # fetch raw proxy
        #     for proxy in getattr(GetFreeProxy, proxyGetter.strip())():
        #         if proxy.strip():
        #             self.log.info('{func}: fetch proxy {proxy}'.format(func=proxyGetter, proxy=proxy))
        #             proxy_set.add(proxy.strip())

        #     # store raw proxy
        #     self.db.changeTable(self.raw_proxy_queue)
        #     for proxy in proxy_set:
        #         self.db.put(proxy)

    def get(self):
        """
        return a useful proxy
        :return:
        """
        # self.db.changeTable(self.useful_proxy_queue)
        # return self.db.get()
        p = self.db.get()
        if not p:
            self.refresh()
            p = self.db.get()
        return p


    def delete(self, proxy):
        """
        delete proxy from pool
        :param proxy:
        :return:
        """
        # self.db.changeTable(self.useful_proxy_queue)
        self.db.rem(proxy)
        pass

    def getAll(self):
        """
        get all proxy from pool
        :return:
        """
        proxies = []
        for ip in self.db.getAll():
            proxies.append(str(ip, "utf-8"))
        return proxies

    def get_status(self):
        # self.db.changeTable(self.raw_proxy_queue)
        # total_raw_proxy = self.db.get_status()
        # self.db.changeTable(self.useful_proxy_queue)
        # total_useful_queue = self.db.get_status()
        # return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}
        pass

if __name__ == '__main__':
    pp = ProxyManager()
    print(pp.getAll())
