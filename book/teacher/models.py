from django.db import models

# Create your models here.


class Student(models.Model):
    '''这是一个学生类'''

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    classroom = models.ForeignKey(to='Classroom')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'

class Classroom(models.Model):
    '''
    这是一个班级类
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'

class Teacher(models.Model):
    '''这是一个教师类'''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    classroom = models.ManyToManyField(to='Classroom')
    # 4.班级和学生是一对多的关系；班级和老师是多对多的关系

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '老师'
        verbose_name_plural = '老师'
    def show_class(self):
        return '|'.join([i.name for i in self.classroom.all()])

