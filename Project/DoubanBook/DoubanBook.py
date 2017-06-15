import random
import datetime
import requests
import xlwt
import xlrd
from bs4 import BeautifulSoup
import multiprocessing
import logging
import time

handler = logging.FileHandler('proxy.log')
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

user_agents = [ 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
	, 'Opera/9.25 (Windows NT 5.1; U; en)'
	, 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
	, 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)'
	, 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12'
	, 'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
	, "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7"
	, "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
	]

https_proxies = []
http_proxies = []
ip_filename = 'ip.xls'

def get_headers():
	return {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding':'gzip, deflate, br',
		'Connection':'keep-alive',
		'User-Agent': random.choice(user_agents),
	}


def get_page(url):
	try:
		return BeautifulSoup(requests.get(url=url, headers=get_headers(), timeout = 3).text, 'lxml')
	# except requests.exceptions.Timeout as e:
	except requests.exceptions.RequestException as e:
		logger.warning('fail to get:', url)
		
	return BeautifulSoup('', 'lxml')


def valid_proxy(proxy):
	proxies = { "http": proxy['addr'] }
	url = '''http://book.douban.com'''
	page = None
	try:
		page = requests.get(url=url, headers=get_headers(), proxies=proxies, timeout=10).text
		isValid = True
	except requests.exceptions.ProxyError as e:
		logger.info('check proxy(%s): ProxyError'%(proxy['addr'], ))
		return False
	except requests.exceptions.Timeout:
		logger.info('check proxy(%s): Timeout'%(proxy['addr'], ))
		return False
	except requests.exceptions.RequestException:
		logger.info('check proxy(%s): RequestException'%(proxy['addr'], ))
		return False
	logger.info('check proxy(%s): valid'%(proxy['addr'], ))
	return True


def get_valid_proxy(proxy_list):
	pool = multiprocessing.Pool(processes = 4)
	result = []
	for p in proxy_list:
		result.append({'res': pool.apply_async(valid_proxy, (p, ))
			, 'proxy': p
		})
	pool.close()
	pool.join()
	for r in result:
		if r['res'].get():
			yield r['proxy']


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

def save_to_excel(filename, proxy_list):
	book = xlwt.Workbook()
	sht = book.add_sheet(datetime.datetime.now().strftime('%Y-%b-%d'), cell_overwrite_ok=True)
	for i, p in enumerate(proxy_list):
		sht.write(i, 0, p['addr'])
		sht.write(i, 1, p['src'])
	book.save(filename)

def get_proxy_from_file(filename):
	sh = xlrd.open_workbook(filename).sheet_by_index(0)
	for r in range(sh.nrows):
		yield {'addr': sh.cell(r, 0).value, 'src': sh.cell(r, 1).value}

def init_proxy():
	pool = multiprocessing.Pool(processes=4)
	funclist = [get_xici_proxy, get_kuai_proxy, get_360_proxy]

	result = []
	for func in funclist:
		result.append(pool.apply_async(func, ()))

	pool.close()
	pool.join()

	proxy_list = []
	for re in result:
		proxy_list.extend(re.get())

	logger.info('Count of total proxy: %d' % len(proxy_list))
	save_to_excel(ip_filename, proxy_list)



def getBook(no):
	url = '''http://book.douban.com/subject/%d/''' % no
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding':'gzip, deflate, br',
		'Connection':'keep-alive',
		# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0', 
		'User-Agent': random.choice(user_agents),
		# 'Cookie':'ll="108296"; bid=7axOkveFIak; push_noty_num=0; push_doumail_num=0; ap=1; dbcl2="41506953:e24+NZ2Ppmg"; ck=Ehwa',
	}



	page = ''
	while len(https_proxies) and len(http_proxies):
		proxies = { "http": random.choice(http_proxies)
			, "https": random.choice(https_proxies)}  
		print(proxies)
		try:
			page = requests.get(url=url, headers=headers, proxies=proxies).text
			break
		except requests.exceptions.ProxyError:
			http_proxies.remove(proxies["http"])
			https_proxies.remove(proxies["https"])
	else :
		return

	bs = BeautifulSoup(page, 'lxml')
	title = bs.find('h1')
	if not title:
		print('no book for %d' % no)
		return
	print('***book for %d: %s' % (no, title))
	# print(r.text)



def getTags(no):
	tag_page = '''https://book.douban.com/tag/?view=type&icn=index-sorttags-all'''
	r = requests.get(url=tag_page)
	bs = BeautifulSoup(r.text, 'lxml')

	for i, td in enumerate(bs.find_all('td')):
		if td.b:
			b = td.b
			print(type(b))
			print(type(b.string))
			print(b.string)


if __name__ == '__main__':
	proxy_list = get_proxy_from_file(ip_filename)
	valid_proxy_list = get_valid_proxy(proxy_list)
	save_to_excel('valid_proxy1.xls', valid_proxy_list)
	logger.info('Count of valid proxy: %d' % len(valid_proxy_list))
	# init_proxy()
	# print(http_proxies)
