# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyDB.py  
   Description :  
   Author :
   date： 
-------------------------------------------------
   Change Activity:
-------------------------------------------------
"""
__author__ = 'Hammurabi'

import sys
import random
import redis

__key_name__ = 'ip_proxy'
__lock_for_write__ = 'lock'

class ProxyDB(object):
    """docstring for ProxyDB"""
    def __init__(self):
        super(ProxyDB, self).__init__()
        self.redis_conn = redis.Redis(host='127.0.0.1', port=6379,db=0)


    def add(self, ip):
        self.redis_conn.sadd(__key_name__, ip)
        pass

    def get(self):
        ips = list(self.redis_conn.smembers(__key_name__))
        if ips:
            return random.choice(list(ips))
        else:
            return None


    def getAll(self):
        ips = self.redis_conn.smembers(__key_name__)
        return list(ips)


    def clear(self):
        return self.redis_conn.delete(__key_name__)


    def unlock(self):
        self.redis_conn.set(__lock_for_write__, 0)
        print(self.redis_conn.get(__lock_for_write__))


    def lockForWrite(self):
        if int(self.redis_conn.get(__lock_for_write__)) == 0:
            self.redis_conn.set(__lock_for_write__, 1)
            return True
        else:
            return False

    def rem(self, ip):
        return self.redis_conn.srem(__key_name__, ip)


def function():
    pass

def run():
    db = ProxyDB()
    if db.lockForWrite():
        db.add(123)
        db.unlock()
    pass

if __name__ == '__main__':
    run()
