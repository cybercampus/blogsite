from django.contrib import admin

# Register your models here.
from .models import Category, Post, Tag, Sidebar

admin.site.register(Category)

admin.site.register(Tag)
admin.site.register(Sidebar)

#文章详情管理
class PostAdmin(admin.ModelAdmin):
    list_display=('id','title', 'category','tags','owner','pv','is_hot','pub_date',)    #显示哪些字段
    list_filter = ('owner',)

    search_fields = ('title','desc',)   #在哪些字段中搜索
    list_editable = ('is_hot',)
    list_display_links = ('title',) #哪些字段加链接

    class Media:
        css = {
            'all':('ckeditor5/cked.css',)   #在页面中引入css文件
        }
        js=(
            'https://cdn.bootcdn.net/ajax/libs/jquery/3.6.3/jquery.js', #在页面中引入js文件
            'ckeditor5/ckeditor.js',
            'ckeditor5/translations/zh.js',
            'ckeditor5/config.js',
        )

admin.site.register(Post, PostAdmin)
