from django.shortcuts import render, HttpResponse, redirect
from app01.models import Person
from app01.forms import Personform
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.


def index(request):
    person_list = Person.objects.all()
    return render(request, 'app01/index.html', {'person_list': person_list})

def edit_person(request):
    # 1-3 获取get 请求id 获取表对象，　实例一个ｆｏｒｍ 对象
    edit_id = request.GET.get('id')
    person_obj = Person.objects.filter(id=edit_id).first()
    form_obj = Personform(instance=person_obj)
    print(edit_id)
    if request.method == 'POST':
        form_obj = Personform(request.POST, instance=person_obj)
        if form_obj.is_valid():
            # 自动修改
            form_obj.save()
            return redirect(reverse('app01:index'))
        else:
            print('2'*10)
            return render(request, 'app01/edit_person.html', {'form_obj': form_obj, 'error_msg': '不符合要求'})


    return render(request, 'app01/edit_person.html', {'form_obj': form_obj})


