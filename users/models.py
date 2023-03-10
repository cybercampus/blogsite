from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    USER_GENDER_TYPE={
        ('male','男'),
        ('female','女'),
    }
    owner = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='用户')
    nick_name = models.CharField('昵称',max_length=25,blank=True,default='')
    desc = models.TextField('个人简介',max_length=225,blank=True,default='')
    gexing = models.CharField('个性签名',max_length=125,blank=True,default='')
    birthday = models.DateField('生日',null=True,blank=True)
    gender = models.CharField('性别', max_length=6, choices= USER_GENDER_TYPE, default='male')
    address = models.CharField('地址',max_length=100,blank=True,default='')
    image = models.ImageField(upload_to='images/%Y/%m',default='images/profile.png',max_length=100,verbose_name='用户图像')

    class Meta:
            verbose_name = '用户数据'
            verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username

# 邮箱验证码校验记录
class EmailVerifyRecord(models.Model):
    SEND_TYPE_CHOICE = (
        ('register','注册'),
        ('forget','找回密码')
    )
    code = models.CharField('验证码',max_length=12)
    email = models.EmailField('邮箱', max_length=25)
    send_type = models.CharField(choices=SEND_TYPE_CHOICE, default='register', max_length=20)
    
    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code