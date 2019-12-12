# -*- coding: utf-8 -*- 
# @Time    : 2019/12/10 18:27 
# @Author  : p0st
# @Site    :  
# @File    : my_tags.py.py
# @Software: PyCharm
from django import template
register = template.Library()
@register.filter
def test_filter(value):
    if not 'kobe' in value:
        return value
    values = value.split('kobe')
    print(value)
    return values