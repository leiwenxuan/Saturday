from django.db import models
from mdeditor.fields import MDTextField

# Create your models here.

class ExampleModel(models.Model):
    name = models.CharField(max_length=20)
    content = MDTextField()
    class Meta:
        verbose_name = '我的makedown'
        verbose_name_plural = '我的makedown'


