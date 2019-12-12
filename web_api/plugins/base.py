# -*- coding: utf-8 -*- 
# @Time    : 2019/12/9 17:26 
# @Author  : p0st
# @Site    :  
# @File    : base.py
# @Software: PyCharm

class BasePlugins(object):
    '''
    写入数据库基类
    '''
    def __init__(self,key):
        self.key =key

    def process(self,info,host_object):
        raise NotImplementedError("子类必须实现process方法~")