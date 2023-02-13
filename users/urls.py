from django.urls import path
from . import views

app_name = 'users'  # 定义命名空间，用来区别不同应用之间的链接地址
urlpatterns = [
    path('login',views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('active/<active_code>', views.active_user,name='active_user')
]