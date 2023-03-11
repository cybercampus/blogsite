from django.shortcuts import render, get_object_or_404
from .models import Category, Post
from django.db.models import Q, F
from django.core.paginator import Paginator

# Create your views here.

# 首页
def index(request):
    # 查询blog数据
    post_list = Post.objects.all()
    paginator = Paginator(post_list,5)   #第二个参数2代表每页显示几条数据
    page_number = request.GET.get('page')   #page=1页码
    page_obj = paginator.get_page(page_number)

    context = {'post_list':post_list, 'page_obj':page_obj}

    return render(request, 'blog/index.html', context)

def category_list(request,category_id):
    category = get_object_or_404(Category,id=category_id)
    posts = category.post_set.all()
    paginator = Paginator(posts,5)   #第二个参数2代表每页显示几条数据
    page_number = request.GET.get('page')   #page=1页码
    page_obj = paginator.get_page(page_number)

    context = {'category': category,'page_obj':page_obj}
    return render(request, 'blog/list.html',context)

def post_detail(request, post_id):
    post = get_object_or_404(Post,id=post_id)

    # 用文章 id 实现上下篇
    prev_post = Post.objects.filter(id__lt=post_id).last()
    next_post = Post.objects.filter(id__gt=post_id).first()

    # 用发布日期实现上下篇
    #prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
    #next_post = Post.objects.filter(add_date__gt=post.add_date).first()

    Post.objects.filter(id=post.id).update(pv = F('pv') + 1)

    context = {'post':post,'prev_post': prev_post,'next_post':next_post}
    return render(request, 'blog/detail.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    if not keyword:
        post_list = Post.objects.all()
    else:
        post_list = Post.objects.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
    paginator = Paginator(post_list,5)   #第二个参数2代表每页显示几条数据
    page_number = request.GET.get('page')   #page=1页码
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
    }
    return render(request,'blog/index.html',context)

#文档归档列表页
def archives(request,year,month):
    post_list = Post.objects.filter(add_date__year=year,add_date__month=month)
    paginator = Paginator(post_list,5)   #第二个参数2代表每页显示几条数据
    page_number = request.GET.get('page')   #page=1页码
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj': page_obj,'year':year,'month':month ,'total': paginator.count}
    return render(request,'blog/archives_list.html', context)