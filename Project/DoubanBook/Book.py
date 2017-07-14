#

# -*- coding: utf-8 -*-

import datetime
class Person(object):
	"""docstring for Person"""
	def __init__(self, name=''):
		super(Person, self).__init__()
		self.name = name
		self.nation = ''
		self.des = ''
		self.href = ''


	def __str__(self):
		return str('[%s]%s' % (self.nation, self.name, ))


class Book(object):
	"""docstring for Book"""
	def __init__(self, title = ''):
		super(Book, self).__init__()
		self.id = 0 # 豆瓣上的编号
		self.title = title # 标题
		self.origin_title = title # 标题
		self.sub_title = '' # 副标题
		self.ISBN = 0
		self.author = []
		self.translator = []
		self.publisher = ''
		self.publication_data = datetime.date.today()
		self.page_count = 0
		self.price = 0.0
		self.collection = 0.0
		self.tags = []
		self.score = 0.0
		self.score_cnt = 0


	def __str__(self):
		return str('''id: %d
author: %s''' 
			% (self.id, self.author))
		