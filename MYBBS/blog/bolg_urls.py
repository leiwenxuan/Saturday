
from django.urls import path
from blog import views

urlpatterns = [
    path('pwd/', views.pwd, name='pwd'),
    path(r'index/', views.index, name='index'),
    path(r'index/', views.home, name='home'),


]
