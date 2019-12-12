# -*- coding: utf-8 -*- 
# @Time    : 2019/12/9 15:31 
# @Author  : p0st
# @Site    :  
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url,include
from web_api.views import cmdb_api

urlpatterns = [
    url(r'^cmdb_api/$', cmdb_api.ServerList.as_view()),
    ]
