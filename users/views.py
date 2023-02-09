#users/views.py
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .forms import LoginForm, RegisterForm

# 邮箱登陆注册
class MyBacked(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs ):   #重载authenticate
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):   #加密明文密码
                return user
        except Exception as e:
            return None

def login_view(request):
    if request.method != 'POST':  #判断请求方式
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            #username = request.POST['username'] # request.POST[] 或 request.POST.get() 获取数据
            #password = request.POST['password']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #与数据库中的用户名和密码比对，采用的是哈希值比对，非明文比对
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)   # login方法登录
                return redirect('/admin')    #HttpResponse('登陆成功！')
            else:
                return HttpResponse('登陆失败！')

    context = {'form':form}
    return render(request,'users/login.html',context)

def register(request):
    '''注册试图'''
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit = False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = form.cleaned_data.get('email')
            new_user.save()
            return HttpResponse('注册成功')

    context = {'form': form}
    return render(request, 'users/register.html',context)  