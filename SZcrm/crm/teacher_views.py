from django import views
from crm.models import ClassList
from django.shortcuts import render, redirect, HttpResponse
from crm.forms import ClassForms
from django.urls import reverse


class ClasslistViews(views.View):

    def get(self, request):
        query_set = ClassList.objects.all()

        return render(request, 'class_list.html', {'class_list': query_set})

    def post(self, request):
        return HttpResponse("班级猎豹 post")


def add_list(request, eidt_id=None):
    class_obj = ClassList.objects.filter(id=eidt_id).first()
    form_obj = ClassForms(instance=class_obj)
    if request.method == 'POST':
        form_obj = ClassForms(request.POST, instance=class_obj)
        if form_obj:
            form_obj.save()
            return redirect(reverse('crm:class_list'))
        else:
            return render(request, 'add_class.html', {"form_obj": form_obj})

    return render(request, 'add_class.html', {"form_obj": form_obj})
