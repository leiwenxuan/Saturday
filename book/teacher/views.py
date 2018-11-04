from django.shortcuts import render, HttpResponse, redirect
from teacher import models
# Create your views here.


def class_list(request):
    '''
    这是一个显示班级列表的函数
    :param request:
    :return:
    '''
    class_list = models.Classroom.objects.all()
    print(class_list)
    return render(request, 'teacher/class_list.html', {'class_list': class_list, 'flag_page':'class'})


def add_class(request):
    '''
    这是一个添加班级函数
    :param request:
    :return:
    '''
    print(000)
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        print(class_name)
        models.Classroom.objects.create(name=class_name)
        return redirect('/teacher/class_list/')
    return render(request, 'teacher/add_class.html')


def del_class(request):
    '''
    这是一个删除班级函数
    :param request:
    :return:
    '''
    del_id = request.GET.get('id')
    print(del_id)
    models.Classroom.objects.get(id=del_id).delete()
    class_list = models.Classroom.objects.all()
    return render(request, 'teacher/class_list.html', {'class_list': class_list})

def edit_class(request):
    '''
    这是修改班级函数
    :param request:
    :return:
    '''
    edit_id_get = request.GET.get('id')
    print(edit_id_get, 5555)
    class_edit = models.Classroom.objects.get(id=edit_id_get)

    if request.method == "POST":

        edit_name = request.POST.get('class_name')
        print(edit_name)
        class_edit.name = edit_name
        class_edit.save()
        return redirect('/teacher/class_list/')

    return render(request, 'teacher/edit_class.html', {'class_edit':class_edit} )


def student_list(request):
    '''
    这是学生列表
    :param request:
    :return:
    '''
    student_list = models.Student.objects.all()
    print(1111111111)
    return render(request, 'teacher/student_list.html', {'student_list': student_list, 'flag_page': 'student'})

def add_student(request):
    '''
    这是添加学生
    :param request:
    :return:
    '''
    class_list = models.Classroom.objects.all()
    if request.method == "POST":
        student_name = request.POST.get('student')
        print(student_name)
        class_id = request.POST.get('class_id')
        print(class_id)
        models.Student.objects.create(name=student_name, classroom_id=class_id)
        return redirect('/teacher/student_list/')

    return render(request, 'teacher/add_student.html', {'class_list': class_list})



def del_student(request):
    '''
    这是删除学生函数
    :param request:
    :return:
    '''

    del_id = request.GET.get('id')

    models.Student.objects.get(id=del_id).delete()


    student_list = models.Student.objects.all()
    return render(request, 'teacher/student_list.html', {'student_list': student_list})

def edit_student(request):
    '''
    这是一个修改学生列表
    :param request:
    :return:
    '''
    #获取学生列表
    class_list = models.Classroom.objects.all()
    #获取点击修改按钮的学生ｉｄ
    student_id = request.GET.get('id')
    print(student_id, '这是修改学生函数')
    # 获取要修改的学生名字
    stu_obj = models.Student.objects.get(id=student_id)
    print(stu_obj.name)
    if request.method == "POST":
        #获取提交的学生姓名
        stu_name = request.POST.get('student')
        #获取班级选项
        class_id = request.POST.get('class_id')
        print(class_id)

        stu_obj.name = stu_name
        stu_obj.classroom_id = class_id

        stu_obj.save()
        return redirect('/teacher/student_list/')



    return render(request, 'teacher/edit_student.html', {"class_list": class_list, 'stu_obj': stu_obj})


def teacher_list(request):
    '''
    这是一个老师列表
    :param request:
    :return:
    '''
    teacher_list = models.Teacher.objects.all()

    return render(request, 'teacher/teacher_list.html', {'teacher_list': teacher_list, 'flag_page': 'teacher'})

def add_teacher(request):
    '''
    这是一个添加老师的函数
    :param request:
    :return:
    '''
    class_list = models.Classroom.objects.all()
    if request.method == 'POST':
        name = request.POST.get('teacher')
        print(name)
        class_id = request.POST.getlist("class_id")
        print(class_id)
        obj = models.Teacher.objects.create(name=name)
        obj.classroom.add(*class_id)
        return redirect('/teacher/teacher_list/')

def del_teacher(request):
    '''
    这是一个删除函数
    :param request:
    :return:
    '''
    del_id = request.GET.get('id')
    obj = models.Teacher.objects.get(id=del_id).delete()

    teacher_list = models.Teacher.objects.all()
    return render(request, 'teacher/teacher_list.html', {'teacher_list': teacher_list})

def edit_teacher(request):
    '''
    这是一个修改老师函数
    :param request:
    :return:
    '''
    class_list = models.Classroom.objects.all()
    teacher_id = request.GET.get('id')
    obj = models.Teacher.objects.get(id=teacher_id)
    print(obj)
    if request.method == 'POST':
        #获取修改老师
        name = request.POST.get('teacher')
        print(name)
        class_id= request.POST.getlist('class_id')
        print(class_id)
        obj.name = name
        obj.save()
        obj.classroom.set(class_id)
        return redirect('/teacher/teacher_list/')
    return render(request, 'teacher/edit_teacher.html', {'class_list': class_list, 'teacher': obj})

def amaze(request):
    class_list = models.Classroom.objects.all()
    return render(request, 'teacher/Amaze.html', {'class_list':class_list})







