from django.contrib import admin
from purview import models
# Register your models here.


# admin.site.register(models.UserPurview)
admin.site.register(models.UserInfo)
admin.site.register(models.Role)


@admin.register(models.UserPurview)
class UserPurviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
    list_editable = ['url']
