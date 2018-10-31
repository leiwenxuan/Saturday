from django.contrib import admin
from book import models
# Register your models here.
admin.register(models.Person)
admin.register(models.book)
admin.register(models.Author)

