#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# Purpose: 用于理解单例模式
# Author: Wangb
# Note:
# Last updated on: 2020-06-02

class Dog(object):
    __instance = None
    __init__flag = False

    def __new__(cls,name):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def __init__(self,name):
        if Dog.__init__flag == False:
            self.name = name
            Dog.__init__flag = True

a = Dog("旺财")
print(id(a))
print(a.name)

b = Dog("哮天犬")
print(id(b))
print(b.name)
