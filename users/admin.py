from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, EmailVerifyRecord

# Register your models here.
#取消User的注册
admin.site.unregister(User)

#定义关联对象的样式，StackedInline 为纵向排列每一行， TabularInline 为并排排列
class UserProfileInLine(admin.StackedInline):
    model = UserProfile   #关联的模型

#关联字段在 User 之内编辑，关联进来
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInLine]

#重新注册 User
admin.site.register(User, UserProfileAdmin)

@admin.register(EmailVerifyRecord)
class Admin(admin.ModelAdmin):
    list_display = ('code',)