from django.shortcuts import render, redirect
from rbac import models
from django.urls import reverse
from crm.models import UserProfile

# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get("password")
        user_obj = UserProfile.objects.filter(
            username=username, password=pwd).first()
        print(username, pwd, user_obj)
        if user_obj:
            # 登陆成功
            from rbac.utils import permission
            permission.init(request, user_obj)
            return redirect(reverse('web:customer_list'))

    return render(request, 'login.html')


# TODO: 2018-11-26 2:50
def logout(request):
    print(request.session)
    request.session.flush()
    return redirect(reverse('login'))
