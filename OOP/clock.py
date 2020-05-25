#!/usr/bin/env python
# -*- encoding:utf-8 
# Purpose: 定义一个类描述数字时钟
# Author: Wangb
# Note:
# Last updated on: 20- -
from time import sleep

class Clock(object):
	'''数字时钟'''
	def __init__(self,hour=0,minute=0,second=0):
		self._hour = hour
		self._minute = minute
		self._second = second

	def run(self):
		self._second += 1
		if self._second == 60:
			self._second = 0
			self._minute += 1
			if self._minute == 60:
				self._minute = 0
				self._hour += 1
				if self._hour == 24:
					self._hour = 0

	def show(self):
		#return '{}:{}:{}'.format(self._hour,self._minute,self._second)
		return '{:.2f}:{:.2f}:{:.2f}'.format(self._hour,self._minute,self._second)

def main():
	clock = Clock(23,59,58)
	while True:
		print(clock.show())
		sleep(1)
		clock.run()

if __name__ =='__main__':
	main()
