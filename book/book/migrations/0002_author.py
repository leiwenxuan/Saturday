# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-30 02:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16)),
                ('age', models.ImageField(upload_to='')),
                ('book', models.ManyToManyField(to='book.book')),
            ],
        ),
    ]
