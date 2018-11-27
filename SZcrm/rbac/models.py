from django.db import models
from crm.models import UserProfile
# Create your models here.


# 权限表
class UserPurview(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=80)
    is_menu = models.BooleanField(default=False, verbose_name='菜单')
    icon = models.CharField(max_length=24, null=True, blank=True, verbose_name='图标')

    class Meta:
        verbose_name = '权限控制'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

# 角色表


class Role(models.Model):
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to='UserPurview')
    user = models.ManyToManyField(to=UserProfile, related_name='roles')
    class Meta:
        verbose_name = '角色控制'
        verbose_name_plural = verbose_name



    def __str__(self):
        return self.title
