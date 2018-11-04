from django.contrib import admin
from book import models
# Register your models here.


@admin.register(models.Press)
class PressAdmin(admin.ModelAdmin):
    list_display = ('pname',)


@admin.register(models.book)
class boolAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','age')




