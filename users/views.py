#users/views.py
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':  #判断请求方式
        username = request.POST['username'] # request.POST[] 或 request.POST.get() 获取数据
        password = request.POST['password']
        #与数据库中的用户名和密码比对，采用的是哈希值比对，非明文比对
        #user = authenticate(request, username, password)

    return render(request,'users/login.html')

# Create your views here.
