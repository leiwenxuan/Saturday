from django.contrib import admin
from teacher import models

# Register your models here.

@admin.register(models.Classroom,)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    # def show_class(self,obj):
    #     print(obj.classroom.all())
    #     return [i.name for i in obj.classroom.all()]
    list_display = ("id", 'name', 'show_class')

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'classroom')



