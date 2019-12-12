# -*- coding: utf-8 -*- 
# @Time    : 2019/12/6 17:04 
# @Author  : p0st
# @Site    :  
# @File    : rbac.py
# @Software: PyCharm
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,redirect
from django.conf import settings
import re
class RbacMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        url = request.path_info
        # 白名单校验
        for item in settings.RBAC_WHILE_URL:
            if re.match(item, url):  # 使用正则表达式来匹配url
                return

        # 登录状态校验
        is_Login = request.session.get('is_login')
        if not is_Login:
            return redirect('/login/')


        # 免认证校验
        for item in settings.RBAC_PASS_URL:
            if re.match(item, url):  # 使用正则表达式来匹配url
                return

        # 等添加权限的时候添加上
        # return HttpResponse('没有访问权限，请联系管理员~')

