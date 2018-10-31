from django.db import models

# Create your models here.


# #必须继承models。Model模块
class Person(models.Model):

    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)


class Press(models.Model):
    #出版社应该应该有id 和出版社
    id = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=30)


#day59　书籍表
class book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    press = models.ForeignKey(to='Press')  #ＯＲＭ帮助我们自动关联Ｐｒｅｓｓ表


# 作者
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    age = models.ImageField()   #年龄参数默认
    #ORM帮我们自动创建第三张关系表
    #表里面有author_id 和 book_id
    book = models.ManyToManyField(to='book')


# #作者和书的关系表
# class Author2Book(models.Model):
#     id = models.AutoField(primary_key=True)
#     author = models.ForeignKey(to='Author')
#     book = models.ForeignKey(to="book")