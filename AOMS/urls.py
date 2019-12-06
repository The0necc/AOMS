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
from django.contrib import admin
from web_home import views as web_home_views
urlpatterns = [
    url(r'^asset/', include('web_cmdb.urls')),
    url(r'^login/$', web_home_views.login, name='login'),
    url(r'^home/$', web_home_views.home, name='home'),
    url(r'^logout/$', web_home_views.logout, name='logout'),
    url(r'', web_home_views.login, name='login')
]
