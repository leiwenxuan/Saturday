from django.conf.urls import url
from teacher import views
from django.contrib import admin
urlpatterns =[
    url(r'^admin',admin.site.urls ),
    url(r'^class_list/', views.class_list),
    url(r'^add_class/', views.add_class),
    url(r'^del_class/', views.del_class),
    url(r'^edit_class/', views.edit_class),

    url(r'^student_list/', views.student_list),
    url(r'^add_student/', views.add_student),
    url(r'^del_student/', views.del_student),
    url(r'^edit_student/', views.edit_student),

    url(r'^teacher_list/', views.teacher_list),
    url(r'^add_teacher/', views.add_teacher),
    url(r'del_teacher/', views.del_teacher),
    url(r'edit_teacher/', views.edit_teacher),

    url(r'amaze/', views.amaze)

    # url(r'^', views.class_list),
]