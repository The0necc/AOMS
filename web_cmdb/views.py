from django.shortcuts import render,redirect,HttpResponse
from web_cmdb import models
import hashlib
# Create your views here.
def dashboard(request):

    return render(request,'dashboard.html')

def index(request):
    assets = models.Asset.objects.all()
    return render(request,'index.html',{"assets":assets})

def detail(request,id):
    asset = models.Asset.objects.filter(id=id).first()
    detail_log = models.EventLog.objects.filter(asset_id=id).all()
    return render(request,'detail.html',{"asset":asset,"detail_log":detail_log})

