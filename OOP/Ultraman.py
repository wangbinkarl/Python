#!/usr/bin/env python
# -*- encoding:utf-8 
# Purpose: 定义一个类模拟奥特曼打小怪兽
# Author: Wangb
# Note:
# Last updated on: 20- -
from abc import ABCMeta,abstractmethod
from random import randint,randrange

class Fighter(object):
	__metaclass__ = ABCMeta
	__slots__ = ('_name','_hp')
	def __init__(self,name,hp):
		self._name = name
		self._hp = hp
	@property
	def name(self):
		return self._name
	@property
	def hp(self):
		return self._hp
	@hp.setter
	def hp(self,hp):
		self._hp = hp if hp >= 0 else 0
	@property
	def alive(self):
		return self.hp > 0
	@abstractmethod
	def attack(self,other):
		pass	

class Ultraman(Fighter):
	__slots__ = ('_name','_hp','_mp')

	def __init__(self,name,hp,mp):
		super(Ultraman,self).__init__(name,hp)
		self._mp = mp

	def attack(self,other):
		other.hp -= randint(15,25)
	
	def huge_attack(self,other):
		if self._mp >= 50:
			self._mp -= 50
			injury = other.hp * 3 // 4
			injury = injury if injury >= 50 else 50
			other.hp -= injury
			return True
		else:
			self.attack(other)
			return False

	def magic_attack(self,others):
		if self._mp >= 20:
			self._mp -= 20
			for temp in others:
				if temp.alive:
					temp.hp -= randint(10,15)
			return True
		else:
			return False

	def resume(self):
		incr_point = randint(1,10)
		self._mp += incr_point
		return incr_point

	def __str__(self):
		return ' {}奥特曼 生命值：{}  魔法值：{}\n'.format(self._name,self._hp,self._mp)

class Monster(Fighter):
	__slots__ = ('_name','_hp')
	def attack(self,other):
		other.hp -= randint(10,20)

	def __str__(self):
		return '{}小怪兽，生命值{}\n'.format(self._name,self._hp)

def is_any_alive(monsters):
	'''判断有没有小怪兽是活着的'''
	for monster in monsters:
		if monster.alive > 0:
			return True
	return False

def select_alive_one(monsters):
	'''选中一只活着的小怪兽'''
	monsters_len = len(monsters)
	while True:
		index = randrange(monsters_len)
		monster = monsters[index]
		if monster.alive >0:
			return monster

def display_info(ultraman,monsters):
	'''显示奥特曼和小怪兽的信息'''
	print(ultraman)
	for monster in monsters:
		print(monster)

def main():
	u = Ultraman('骆昊',1000,120)
	m1 = Monster('狄仁杰',250)
	m2 = Monster('白元芳',250)
	m3 = Monster('王大锤',250)
	ms = [m1,m2,m3]	
	fight_round = 1

	while u.alive and is_any_alive(ms):
		print('===========第{}回合========\n'.format(fight_round))
		m = select_alive_one(ms) '''选中一只小怪兽'''
		skill = randint(1,10) '''通过随机数选择使用哪种技能'''

		if skill <= 6:
			print('{}使用普通攻击打了{}'.format(u.name,m.name))
			u.attack(m)
			print('{}魔法值恢复了{}点'.format(u.name,u.resume()))
		elif skill <= 9:
			if u.magic_attack(ms):
				print('{}使用了魔法攻击'.format(u.name))		
			else:
				print('{}使用魔法失败.'.format(u.name))
		else:
			if u.huge_attack(m):
				print('{}使用必杀技虐了{}'.format(u.name,m.name))
			else:
				print('{} 使用普通攻击了 {}'.format(u.name,m.name))
				print('{} 的魔法值恢复了 {} 点'.format(u.name,u.resume()))
		if m.alive > 0:
			print('{}回击了{}'.format(m.name,u.name))
			m.attack(u)

		display_info(u,ms)
		fight_round += 1
	print("===============战斗结束========\n")
	if u.alive > 0:
		print("{}奥特曼胜利".format(u.name))
	else:
		print('小怪兽胜利')

if __name__ =='__main__':
	main()
