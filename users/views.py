#users/views.py
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from .models import EmailVerifyRecord, UserProfile
from utils.email_send import send_register_mail
from django.contrib.auth.decorators import login_required

# 邮箱登陆注册
class MyBacked(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs ):   #重载authenticate
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):   #加密明文密码
                return user
        except Exception as e:
            return None

#修改用户状态，对比验证码
def active_user(request,active_code):
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save()
        else:
            return HttpResponse('连接有误！')
        return redirect('users:login')

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
                #登陆成功后，跳转到个人中心
                return redirect('users:user_profile')    #HttpResponse('登陆成功！')
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

            send_register_mail(form.cleaned_data.get('email'),'register')
            return HttpResponse('注册成功')

    context = {'form': form}
    return render(request, 'users/register.html',context)   

#填写 email 表单页面，用于发送密码
def forget_pwd(request):
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            exists = User.objects.filter(email=email).exists()  #查询email在数据库中是否存在
            if exists:
                send_register_mail(email,'forget')  #存在，就发送邮件
                return HttpResponse('邮件已发送请查收！')
            else:
                return HttpResponse('邮箱还未注册，请注册！')   #不存在，就转到注册页面
    return render(request, 'users/forget_pwd.html', {'form':form})

def forget_pwd_url(request, active_code):
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse('修改成功！')
        else:
            return HttpResponse('修改失败！')
    return render(request, 'users/reset_pwd.html',{'form':form})

@login_required(login_url='users:login')
def user_profile(request):
    user = User.objects.get(username=request.user)
    print('user:',user) 
    return render(request, 'users/user_profile.html',{'user':user})

def logout_view(request):
    logout(request)
    return redirect('users:login')
