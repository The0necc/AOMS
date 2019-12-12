# -*- coding: utf-8 -*- 
# @Time    : 2019/12/9 9:50 
# @Author  : p0st
# @Site    :  
# @File    : cmdb_api.py
# @Software: PyCharm
import datetime
from web_cmdb import models
from django.shortcuts import render,HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework import serializers
from rest_framework.response import Response
from web_api.plugins import process_info
# from rest_framework.versioning import URLPathVersioning

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = "__all__"

class ServerList(GenericAPIView):
    serializer_class = NewsSerializer  # 序列化
    def post(self,request, *args, **kwargs):
        ip = request.data.get("ip")
        # {'ip': '119.27.179.180', 'info': {'cpu': {'status': True, 'data': {'cpu_count': 1, 'cpu_physical_count': 1, 'cpu_model': ' Intel(R) Xeon(R) CPU E5-26xx v4'}, 'error': None}}}
        info = request.data["info"]
        host_obj = models.Asset.objects.get(ip=ip)
        if not host_obj:
            return Response("主机不存在")
        print(info)
        # process_info(info, host_obj)
        return Response('ok~')

    def get(self, request, *args, **kwargs):
        server_list = models.Asset.objects.all()
        host_info = []
        for item in server_list:
            if item.status==1 and item.c_status==1 and item.asset_type=='server':
                host_info.append(item.ip)
        return Response(host_info)


