import os
import random
import datetime
import requests
import xlwt
import xlrd
from bs4 import BeautifulSoup
import multiprocessing
import subprocess
import logging
import time
import Book
import redis

import sys
sys.path.append('../')

book_html_folder = 'book_html'

handler = logging.FileHandler('book.log')
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


def get_proxy():
	resp = requests.get("http://127.0.0.1:5000/get/")
	while resp.status_code != 200:
		print(resp.status_code)
		time.sleep(10)
		resp = requests.get("http://127.0.0.1:5000/get/") 
	return str(resp.content, 'utf-8')


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5000/delete/?proxy={}".format(proxy))

def getPage(url, check=None):
	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding':'gzip, deflate, br',
		'Connection':'keep-alive',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0', 
		# 'User-Agent': random.choice(user_agents),
	}

	page = ''
	status_code = 0
	while not page:
		ip_proxy = get_proxy()
		proxies = { "http": ip_proxy, "https": ip_proxy}
		try:
			resp = requests.get(url=url, headers=headers, 
				proxies=proxies, timeout=10.0)
			status_code = resp.status_code
			if resp.status_code in [403, 407] :
				raise requests.exceptions.ProxyError()
			if check and not check(resp.text):
				raise requests.exceptions.ProxyError()
			page = resp.text
			break
		except requests.exceptions.ProxyError:
			delete_proxy(ip_proxy)
		except requests.exceptions.RequestException as e:
			delete_proxy(ip_proxy)
	return (status_code, page)

def isValidBookPage(page):
	bs = BeautifulSoup(page, 'lxml')
	h1 = bs.find('h1')
	if not h1:
		return True
	if not h1.string:
		return True
	if 'Unauthorized ...' in h1.string:
		return False
	return True


def fetchBookPage(no):
	url = '''http://book.douban.com/subject/%d/''' % no
	status_code, page = getPage(url, isValidBookPage)

	if status_code == 200:
		with open(os.path.join(book_html_folder, str(no)), 'w', encoding='utf-8') as f:
			f.write(page)
	else:
		page = None
	redis_conn = redis.Redis(host='127.0.0.1', port=6379,db=0)
	redis_conn.set(no, status_code)
	return page


def getBookPage(no):
	file_path = os.path.join(book_html_folder, str(no))
	if os.path.isfile(file_path):
		print('read from file: ', no)
		with open(file_path, 'r', encoding='utf-8') as f:
			page = f.read()
	else:
		page = fetchBookPage(no)
	return page


def getPerson(a_tag):
	p = Book.Person()
	p.href = a_tag['href']
	s_l = str(a_tag.string).strip().split(']')
	if len(s_l) == 1:
		p.name = s_l[0].strip('\n[] ')
	elif len(s_l) == 2:
		p.name = s_l[1].strip('\n[] ')
		p.nation = s_l[0].strip('\n[] ')
	else:
		print('Error : %s' %s (s,))
	return p

def downloadBook(book_url, save_dir):
	book_id = book_url.split('/')[-2]
	file_path = os.path.join(save_dir, book_id)
	if os.path.isfile(file_path):
		print('book ', book_id, ' downloaded already. ')
		return True

	print('downloading book: ', book_id)
	status_code, page = getPage(book_url, isValidBookPage)

	if status_code == 200:
		with open(os.path.join(save_dir, book_id), 'w', encoding='utf-8') as f:
			f.write(page)
			print('book: ', book_id, ' saved. ')
			return True
	return False

def getBook(no): 
	print('get book: ', no)
	redis_conn = redis.Redis(host='127.0.0.1', port=6379,db=0)
	redis_conn.delete(no)
	# if redis_conn.get(no) and (str(redis_conn.get(no), 'utf-8') == NO_BOOK):
	# 	print('no book: ', no)
	# 	return None
	page = getBookPage(no)
	if not page: 
		redis_conn.set(no, NO_BOOK)
		return None
	return None
	bs = BeautifulSoup(page, 'lxml')
	h1 = bs.find('h1')
	if not h1:
		print('no book for %d' % no)
		print(page)
		return
	title = h1.find('span')
	if not title:
		print('no book for %d' % no)
		print(page)
		return
	print('***book %d' % (no,))
	print('title : %s' % (str(title.string).strip(),))
	info_div = bs.find_all('div', id='info')
	if len(info_div) != 1:
		print('Wrong count of info_div: %d', len(info_div))
		return
	span_list = info_div[0].find_all('span', class_='pl')

	bk = Book.Book()
	bk.id = no
	for span in span_list:
		if '作者' in str(span.string):
			par = span.parent
			if par.name == 'div':
				bk.author.append(getPerson(span.next_sibling.next_sibling))
				pass
			elif par.name == 'span':
				for t in span.parent.find_all('a', class_=''):
					bk.author.append(getPerson(t))
			# for a in bk.author:
			# 	print(a)
		elif '出版社' in str(span.string):
			bk.publisher =  str(span.next_sibling).strip()
			# print('publisher: ', str(span.next_sibling).strip())
		elif '副标题' in str(span.string):
			bk.sub_title =  str(span.next_sibling).strip()
			# print('sub title: ', str(span.next_sibling).strip())
		elif '出版年' in str(span.string):
			s = str(span.next_sibling).strip()
			d = datetime.date(1800, 1, 1)
			try:
				lst = s.split('-')
				if len(lst) == 3:
					d = datetime.date(int(lst[0]), int(lst[1]), int(lst[2]))
				elif len(lst) == 2:
					d = datetime.date(int(lst[0]), int(lst[1]), 1)
				elif len(lst) == 1:
					d = datetime.date(int(lst[0]), 1, 1)
			except Exception as e:
				print(s, e)
				pass
			bk.publication_data = d
			print(bk.publication_data)
		elif '页数' in str(span.string):
			pass
			bk.page =  str(span.next_sibling).strip()
			# print('page: ', str(span.next_sibling).strip())
		elif '定价' in str(span.string):
			s = str(span.next_sibling)
			try:
				bk.price = float(s.strip('元cnyCNY \n'))
			except Exception as e:
				print(s, e)
				pass
			# print(bk.price)
		elif '装帧' in str(span.string):
			pass
			# print('zhuang zhen: ', str(span.next_sibling).strip())
		elif 'ISBN' in str(span.string):
			bk.ISBN = int(str(span.next_sibling).strip())
		elif '译者' in str(span.string):
			# todo
			pass
		elif '原作名' in str(span.string):
			bk.origin_title = str(span.next_sibling).strip()
			print(bk.origin_title)
			pass
		elif '丛书' in str(span.string):
			# todo
			pass
		else:
			logger.warning('Unhandled property: %d, %s' % (no, span.string.strip(),))
			pass

	return bk

	# print(len(lst))
	# for t in lst:
	# 	print(str(t.string), str(t.next_sibling.string))
	# 	print(str(t.next_sibling.next_sibling.string))
	# print('author : %s' % (str(title.string).strip(),))



# def check(no):
# 	redis_conn = redis.Redis(host='127.0.0.1', port=6379,db=0)
# 	if int(redis_conn.get(no)) == 200:
# 		if not isValidBookPage(getBookPage(no)):
# 			redis_conn.delete(no)
# 			file_path = os.path.join(book_html_folder, str(no))
# 			if os.path.isfile(file_path):
# 				os.remove(file_path)

# 	pass
def setDownloading(book_tag, loading = True):
	redis_conn = redis.Redis(host='127.0.0.1', port=6379,db=0)
	redis_conn.set(book_tag+'loading', 1 if loading else 0)

def getDownloading(book_tag):
	redis_conn = redis.Redis(host='127.0.0.1', port=6379,db=0)
	return int(redis_conn.get(book_tag+'loading')) == 1

def getBookID(book_tag):
	print('start fetch %s.' % (book_tag, ))
	setDownloading(book_tag)
	url = '''https://book.douban.com/tag/%s?type=S''' % (book_tag, )
	page_idx = 0
	book_cnt = 0
	while True:
		page_idx = page_idx + 1
		status_code, page = getPage(url)
		bs = BeautifulSoup(page, 'lxml')
		div_list = bs.find_all('div', class_='info')
		print('producer: %d on page %d.' % (len(div_list), page_idx,))
		book_cnt = book_cnt + len(div_list)
		redis_conn = redis.Redis(host='127.0.0.1', port=6379,db=0)
		for div in div_list:
			a = div.find('h2').find('a')
			redis_conn.sadd(book_tag, a['href'])

		next_page = bs.find('a', string='后页>')
		if not next_page:
			break
		url = 'https://book.douban.com' + next_page['href']
	setDownloading(book_tag, False)
	print('*'*20)
	print('%d/% fon %s.' % (book_cnt, page_idx, book_tag, ))

def downloadTag(tag_name):
	tag_dir = os.path.join(book_html_folder, tag_name)
	if not os.path.isdir(tag_dir):
		os.mkdir(tag_dir)
	print(tag_name, ' comsumer')
	while True:
		redis_conn = redis.Redis(host='127.0.0.1', port=6379,db=0)
		url = redis_conn.spop(tag_name)
		if url:
			if downloadBook(str(url, 'utf-8'), tag_dir):
				pass
			else:
				redis_conn.sadd(tag_name, url)
		else:
			if getDownloading(tag_name):
				print(tag_name, ' wait')
				time.sleep(10)
				print(tag_name, ' wake up')
				continue
			else:
				break
	print(tag_name, ' comsumer end')


def getTags():
	tag_page = '''https://book.douban.com/tag/?view=type'''
	r = requests.get(url=tag_page)
	bs = BeautifulSoup(r.text, 'lxml')
	for i, td in enumerate(bs.find_all('td')):
		if td.b:
			b = td.b
			print(str(td.a.string))



if __name__ == '__main__':
	tags = ['社会学', '艺术','设计','社会','政治','建筑','宗教','电影','数学','政治学','回忆录','中国历史','思想','国学','音乐','人文','人物传记','绘画','戏剧','艺术史','佛教','军事','西方哲学','二战','近代史']
	tags = ['中国历史','国学','人文','军事','西方哲学','近代史']


	for tag_name in tags:
		pool = multiprocessing.Pool(processes=3)
		pool.apply_async(getBookID, (tag_name,))
		pool.apply_async(downloadTag, (tag_name,))
		pool.apply_async(downloadTag, (tag_name,))
		pool.close()
		pool.join()

	# p = subprocess.Popen(
	# 	'echo %s | sudo -S shutdown now',
	# 	shell = True,
	# 	close_fds = True,
	# 	stdin=subprocess.PIPE,
	# 	stdout=subprocess.PIPE)

	# no = 1675478 # tian chao de beng kui
	# no = 19920715 # on china
	# getBook(no)
	# no = 1929984 # shu ju ku 
	# getBook(no)
	# no = 26598142 # hu pan
	# getBook(no)

