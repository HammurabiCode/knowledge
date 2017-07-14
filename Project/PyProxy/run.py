import os
import platform

import ProxyDB
import ProxyApi
import multiprocessing
import subprocess

def checkDB(program, port):
	'''
		check port 6357 & process redis-server
	'''
	p = subprocess.Popen(
		'echo %s | sudo -S netstat -naop | grep %d' %('helloworld', port),
		shell = True,
		close_fds = True,
		stdin=subprocess.PIPE,
		stdout=subprocess.PIPE)
	# p.stdin.write(b'helloworld\n')
	res = str(p.stdout.read(), 'utf-8')
	for s in res.split(' '):
		if program in s:
			return True
			# print(s.split('/')[0])
	return False

if __name__ == '__main__':
	# database
	if not checkDB('redis-server', 6379):
		print('Redis Server is not running. Start it.') 
		multiprocessing.Process(target = ProxyDB.run).start()
	else:
		print('Redis Server is running.') 

	if not checkDB('python', 5000):
		print('Proxy Server is not running. Start it.') 
		multiprocessing.Process(target = ProxyApi.run).start()
	else:
		print('Proxy Server is running.') 
