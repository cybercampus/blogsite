# 在这里自定义模板标签
from django import template
from blog.models import Category, Sidebar, Post

register = template.Library()   # 注意，此处 Library 首字母要大写

# 全站的分类
@register.simple_tag
def get_category_list():
    return Category.objects.all()

# 全站的侧边栏
@register.simple_tag
def get_sidebar_list():
    return Sidebar.get_sidebar()

# 最新文章
@register.simple_tag
def get_new_post():
    return Post.objects.order_by('-pub_date')[:6]

# 热门文章
@register.simple_tag
def get_hot_post():
    return Post.objects.filter(is_hot=True)[:6]

# 热门文章
@register.simple_tag
def get_hot_pv_post():
    return Post.objects.order_by('-pv')[:6]

# 文章归档
@register.simple_tag
def get_archives():
    return Post.objects.dates('add_date', 'month', order='DESC')[:6]    #dates的查询方法，返回日期字段的对应年，月，日