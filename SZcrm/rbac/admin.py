from django.contrib import admin
from rbac import models
# Register your models here.


@admin.register(models.UserPurview)
class UserPurviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_menu', 'icon']
    list_editable = ['url', 'icon', 'is_menu']


@admin.register(models.Role)
class UserPurviewAdmin(admin.ModelAdmin):
    list_display = ['title']
