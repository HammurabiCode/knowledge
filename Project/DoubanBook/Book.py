#

# -*- coding: utf-8 -*-

import datetime
class Person(object):
	"""docstring for Person"""
	def __init__(self, name, nation):
		super(Person, self).__init__()
		self.name = name
		self.nation = ''


class Book(object):
	"""docstring for Book"""
	def __init__(self, name):
		super(Book, self).__init__()
		self.name = name
		self.ISBN = 0
		self.sub_title = ''
		self.author = []
		self.translator = []
		self.publisher = ''
		self.publication_data = datetime.date()
		self.page_count = 0
		self.price = 0.0
		self.collection = 0.0
		