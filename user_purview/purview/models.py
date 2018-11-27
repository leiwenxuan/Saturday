from django.db import models

# Create your models here.


# 权限表
class UserPurview(models.Model):
    title = models.CharField(max_length=12)
    url = models.CharField(max_length=22)
    class Meta:
        verbose_name = '权限控制'
        verbose_name_plural = verbose_name

# 用户表
class UserInfo(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=12)
    role = models.ManyToManyField(to='Role')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


# 角色表
class Role(models.Model):
    title = models.CharField(max_length=12)
    permissions = models.ManyToManyField(to=UserPurview)

    class Meta:
        verbose_name = '角色控制'
        verbose_name_plural = verbose_name

