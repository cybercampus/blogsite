from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=32, widget=forms.TextInput(attrs={
        'class':'input', 'placeholder':'用户名/邮箱'
    }))
    password = forms.CharField(label='密码', max_length=6, widget=forms.PasswordInput(attrs={
        'class':'input', 'placeholder':'密码'
    }))
    
    # 对 username, password进行验证
    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username == password:
            raise forms.ValidationError('用户名和密码不能相同！')

        return password

# 使用 Django 提供的 ModelForm 实现注册页面
class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='密码', max_length=6, widget=forms.PasswordInput(attrs={
        'class':'input', 'placeholder':'密码'
    }))
    password1 = forms.CharField(label='确认密码', max_length=6, widget=forms.PasswordInput(attrs={
        'class':'input', 'placeholder':'确认密码'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')    #设置允许被编辑的字段名称

    '''验证用户名是否已存在'''
    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username)
        if exists:
            raise forms.ValidationError('用户名已存在！')
        return username

    def clean_password1(self):
        """验证密码是否一致"""
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password != password1:
            raise forms.ValidationError('密码不一直！')
        return self.cleaned_data.get('password1')
