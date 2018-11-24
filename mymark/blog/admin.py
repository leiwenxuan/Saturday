from django.contrib import admin

# Register your models here.
from blog import models

admin.register(models.MDTextField)
from django.contrib import admin

# Register your models here.


admin.site.site_header = '无言后台管理'
admin.site.site_title = '孤独'


@admin.register(models.ExampleModel)
class ExampleModelAdmin(admin.ModelAdmin):
    list_display = ('name',)


