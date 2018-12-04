from django.conf.urls import url
from bbs import views

urlpatterns = [url(r'^login/$', views.login, name='login')]
