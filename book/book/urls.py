
from django.conf.urls import url
from book import views
from book.views import index, login, edit_press, add_press,del_press
from book import views
app_name = 'book'
urlpatterns = [
    url(r'^index', index, name='index'),
    url(r'^login', login),
    url(r'^add_press', add_press),
    url(r'^edit_press', edit_press),
    url(r'^del_press', del_press),
    url(r'^book_list', views.book_list),

    url(r'^add_book', views.add_book),
    url(r'^del_book', views.del_book),
    url(r'^edit_book', views.edit_book),


    #__________day59-----------

    url(r'^author_list', views.author_list, name='author_list'),
    url(r'^add_author', views.add_author),
    url(r'^del_author', views.del_author),
    url(r'^edit_author', views.edit_author),
    url(r'^test', views.test),
    url(r'^template_test', views.template_test),
   url(r'^birthday', views.birthday),
    url(r'', views.book_list)
]