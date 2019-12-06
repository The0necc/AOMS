# -*- coding: utf-8 -*- 
# @Time    : 2019/12/5 19:22 
# @Author  : p0st
# @Site    :  
# @File    : urls.py
# @Software: PyCharm

"""AOMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from web_cmdb import views as web_cmdb_views
urlpatterns = [
    url(r'^dashboard/$', web_cmdb_views.dashboard,name='asset/dashboard'),
    url(r'^index/$', web_cmdb_views.index,name='asset/index'),
    url(r'^detail/(?P<id>\w+)/$', web_cmdb_views.detail,name='asset/detail'),
]
