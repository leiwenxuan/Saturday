from django.contrib import admin
from blog import models

# Register your models here.


@admin.register(models.UserInfo)
class UserinfoAdmin(admin.ModelAdmin):
    '''用户信息'''
    exclude = ('', )


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    '''博客信息'''
    exclude = ('', )


@admin.register(models.Category)
class GategoryAdmin(admin.ModelAdmin):
    """
      个人博客文章分类
      """
    exclude = ('', )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    """
    标签
    """
    exclude = ('', )


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    """
       文章
       """
    exclude = ('', )


@admin.register(models.ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    """
     文章详情表
     """
    exclude = ('', )


@admin.register(models.ArticleUpDown)
class ArticleUpDownAdmin(admin.ModelAdmin):
    """
    点赞表
    """
    exclude = ('', )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    exclude = ('', )
