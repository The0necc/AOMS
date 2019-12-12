from django.shortcuts import render,redirect
import hashlib
from web_cmdb import models
# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    md5 = hashlib.md5()  # 选择一个要加密的方式
    md5.update(password.encode('utf-8'))  # 将要加密的内容格使用选择后的方法进行加密
    md5_password = md5.hexdigest()
    user_obj = models.User.objects.filter(username=username,password=md5_password).first()
    # print(username,md5_password,user_obj)
    if user_obj:
        request.session['is_login'] = True
        request.session['user_id'] = user_obj.id
        return redirect('/home/')
        # return render(request,'home.html')
    return render(request, 'login.html', {'error': '用户名或密码错误~'})

def home(request):
    return render(request,'home.html')

def logout(request):
    request.session.flush()
    return redirect('/login/')