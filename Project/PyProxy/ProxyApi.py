# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyApi.py  
   Description :  
   Author :
   date： 
-------------------------------------------------
   Change Activity:
-------------------------------------------------
"""
__author__ = 'Hammurabi'

import sys

from flask import Flask, jsonify, request
import ProxyManager

app = Flask(__name__)

api_list = {
    'get': u'get an usable proxy',
    'refresh': u'refresh proxy pool',
    'get_all': u'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:8080': u'delete an unable proxy',
}


@app.route('/')
def index():
    return jsonify(api_list)


@app.route('/get/')
def get():
    proxy = ProxyManager.ProxyManager().get()
    print(proxy)
    return proxy

@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    ProxyManager.ProxyManager().delete(proxy)
    return 'success'

@app.route('/refresh/')
def refresh():
    # TODO refresh会有守护程序定时执行，由api直接调用性能较差，暂不使用
    ProxyManager.ProxyManager().refresh()
    return 'success'


@app.route('/get_all/')
def getAll():
    proxies = ProxyManager.ProxyManager().getAll()
    return jsonify(list(proxies))



@app.route('/get_status/')
def get_status():
    # status = ProxyManager().get_status()
    return jsonify(status)


def run():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run()