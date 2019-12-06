from django.shortcuts import render,redirect
from web_cmdb import models
import hashlib
# Create your views here.
def dashboard(request):

    return render(request,'dashboard.html')

def index(request):

    return render(request,'index.html')

def detail(request,id):

    return render(request,'detail.html')

