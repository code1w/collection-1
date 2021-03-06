#! /usr/bin/env python
# -*- coding: utf-8 -*-
#======================================================================
#
# fiction_zhuaji.py - zhuaji.org fiction download
#
# Created by skywind on 2016/11/29
# Last change: 2016/11/29 17:33:34
#
#======================================================================
import shell
import re


class FictionZhuaJi (object):

	def __init__ (self, url):
		self._url = url
		self._content = shell.request_safe(url).decode('gbk', 'ignore')
		#self._content = open('content.txt', 'r').read().decode('gbk')
		content = self._content
		p = re.compile(r'<dd><a\shref="(\d*.html)" title="(.*)"')
		result = [[0, x[0], x[1]] for x in p.findall(content)]
		for m in result:
			m[0] = int(re.findall('\d*', m[1])[0])
		result.sort()
		self._index = [(m[1], m[2]) for m in result]
		p1 = content.find('<div class="mulu_bookinfo">')
		p2 = content.find('</div>', p1)
		intro = ''
		if p1 >= 0 and p2 >= 0:
			text = content[p1:p2]
			intro = shell.html2text(text) + '\n\n'
		self._intro = intro

	def __len__ (self):
		return len(self._index)

	def __getitem__ (self, n):
		return self._index[n][1]

	def read_chapter (self, n):
		if self._url[-1] == '/':
			url = self._url + self._index[n][0]
		else:
			url = self._url + '/' + self._index[n][0]
		return shell.request_safe(url).decode('gbk', 'ignore')

	def chapter (self, n):
		content = self.read_chapter(n)
		p = re.compile(r'<div id="content">(.*)</div>')
		result = p.findall(content)
		html = result[0]
		return shell.html2text(html)

	def download (self, filename):
		part = []
		size = len(self._index)
		for i in xrange(size):
			text = self._index[i][1] + '\n\n'
			print '[%d/%d] %s'%(i + 1, size, self._index[i][1])
			text+= self.chapter(i) + '\n\n'
			part.append(text)
			import time
			#time.sleep(2)
		text = '\n'.join(part)
		self._whole = self._intro + text
		open(filename, 'w').write(self._whole.encode('utf-8'))
		print 'saved:', filename
		return 0



#----------------------------------------------------------------------
# simple download interface
#----------------------------------------------------------------------
def download (url, filename):
	zj = FictionZhuaJi(url)
	zj.download(filename)
	return 0


#----------------------------------------------------------------------
# main program
#----------------------------------------------------------------------
if __name__ == '__main__':
	url = 'http://www.zhuaji.org/read/179/'

	def test1():
		zj = FictionZhuaJi(url)
		#print zj.chapter(0)
		return 0

	def test2():
		download(url, 'e:/fiction.txt')
		return 0

	test2()


