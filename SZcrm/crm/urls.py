from django.conf.urls import url
from crm import views
from crm.teacher_views import ClasslistViews, add_list

urlpatterns = [

    url(r'^login/', views.LoginViews.as_view(), name='login'),
    url(r'^log/', views.login, name='log'),

    url(r'^reg/', views.RegViews.as_view(), name='reg'),
    url(r'^index1/', views.IndexViews.as_view(), name='index1'),
    url(r'^cus_list/', views.IndexViews.as_view(), name='cus_list'),
    url(r'^check_user/', views.check_user, name='check_user'),
    url(r'^logout/', views.Logout.as_view(), name='logout'),
    url(r'^change/', views.ChangeVires.as_view(), name='change'),
    url(r'^add/$', views.Add_cus.as_view(), name='add_cus'),
    url(r'^edit_cus/(\d+)$', views.Add_cus.as_view(), name='add_cus'),

    url(r'^get_valid_img.png/', views.get_valid_img),

    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register/', views.get_geetest),

    url(r'^private/', views.IndexViews.as_view(), name='pirvate'),

    url(r'record_list/', views.record_list, name='record_list'),
    url(r'change_recode/', views.change_record, name='change_record'),
    url(r'enrollment/(?P<customer_id>\d+)/$', views.EnrollmentViews.as_view(), name='enrollment'),
    url(r'enr_edit/(?P<customer_id>\d+)$', views.enr_editViews.as_view(), name='enr_edit'),
    url(r'enr_edit/(?P<enrollment_id>\d+)$', views.enr_editViews.as_view(), name='enr_edit'),


    # 班级url视图
    url(r'class_list', ClasslistViews.as_view(), name='class_list'),
    url(r'add_class/(\d+)$', add_list, name='add_list')


]
