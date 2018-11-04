from django.shortcuts import HttpResponse, render, redirect
from book.models import Press, book, Person, Author
import logging
logger = logging.getLogger(__name__)

def login(request):
    #定义一个error 消息替换变量
    error_msg = ''
    # 如果是POST提交
    if request.method == "POST":
        # request.POST提交的字典的形式
        email = request.POST['email']
        # 字典操作get 没有找到返回None
        pwd = request.POST.get('pwd',None)

        ret = Person.objects.filter(email=email, password=pwd)
        # if email == '892028617@qq.com' and pwd == '123':
        if ret:
            return redirect('/book/author_list/')
        else:
            error_msg = '用户名和密码错误'
    # 如果用户验证正确那么error_msg 是空字符串 为空render不出来
    return render(request, 'book/login.html', {'error_msg':error_msg})


def index(request):

    data = Press.objects.all()
    # print(data[0].pname)

    return render(request,'book/index.html', {"press_list": data})


def add_press(request):
    print(1111)
    if request.method == "POST":
        ret = request.POST.get("press_name")
        Press.objects.create(pname=ret)
        print(333)
        return redirect("/book/index.html/")
    return  render(request, 'book/add_press.html',)


def del_press(request):
    #获取ID
    del_id = request.GET.get("id")
    print(del_id)
    Press.objects.filter(id=del_id).delete()

    return redirect("/book/index.html/")


def edit_press(request):
    print("*"*120)
    #先查询表单ｎａｍｅ
    if request.method == "POST":
        id = request.POST.get("press_id")
        name = request.POST.get("press_name")
        ret = Press.objects.get(id=id)
        ret1 =  Press.objects.filter(id=id)
        ret.pname = name
        ret.save()
        return redirect("/book/index.html/")
    id_edit = request.GET.get('id')
    print(id_edit)
    print("*" * 120)
    obj = Press.objects.get(id=id_edit)
    print("*" * 120)
    return render(request, "book/edit_press.html", {"obj":obj})


def test():
    def foo(func):
        def bar(*args, **kwargs):
            ret = Person.objects.all()
            if ret:
                return HttpResponse("密码错误")

            else:
                return redirect('/book/login/')
        return bar
    return foo



def book_list(request):
    ret = book.objects.all()
    press_ret = Press.objects.all()
    print(press_ret)
    return render(request, 'book/book_list.html', {"book_list": ret, "press_list": press_ret})


#添加数据
def add_book(request):
    add_name = request.POST.get('book_name')
    add_press = request.POST.get('press')
    print(add_press, add_name)
    book.objects.create(title=add_name, press_id=add_press)
    ret_press = Press.objects.all()
    return redirect("/book/book_list.html/")



#删除图书
def del_book(requesst):

    book_id = requesst.GET.get("id")
    print('你要删除我吗', book_id)
    book.objects.filter(id=book_id).delete()
    return redirect('/book/book_list.html/')


def edit_book(request):
    book_id = request.GET.get('id')
    print(book_id)
    ret_press = Press.objects.all()
    edit_book = book.objects.get(id=book_id)
    if request.method == "POST":
        print(12333333)
        press_input =  request.POST.get('press_name')
        book_input = request.POST.get('title')
        print(press_input, book_input)
        edit_book.title=book_input
        edit_book.press_id = press_input
        edit_book.save()
        return redirect('/book/book_list/')
    return render( request, 'book/edit_book.html', {"press_list": ret_press, 'book': edit_book})


#day59　作者

def author_list(request):
    author_obj = Author.objects.all()

    press_list = Press.objects.all()
    book_list = book.objects.all()
    return render(request, 'book/author_list.html', {"author_list":author_obj, 'press_lisst':press_list, 'book_list': book_list})

# 添加作者
def add_author(request):
    if request.method == 'POST':
        author_name = request.POST.get("author_name")
        author_age = request.POST.get("author_age")
        book_list = request.POST.getlist("book_name")
        print(book_list)
        #创建新的桌表
        obj = Author.objects.create(name=author_name, age=author_age)
        print(obj, type(obj))
        obj.book.add(*book_list)  #给创建的作者对象添加关联的书籍信息
        #上面的操作本质上在三张表建立了许多新的关联对象
        return redirect('/book/author_list/')

        #1 创建一个新的作者和书关系表
    return HttpResponse("KO")

#　删除作者
def del_author(request):
    del_id= request.GET.get("id")
    print(del_id)
    Author.objects.filter(id=del_id).delete()

    return redirect('/book/author_list/')

# 编辑作者
def edit_author(request):
    # 要在页面显示修改的选项，　需要有当前的作者，　当前图书信息，　和　出版社信息
    # 出版社对象
    press_list = Press.objects.all()
    # 书籍对象
    book_list = book.objects.all()
    # 作者对象
    author_id = request.GET.get('id')
    author = Author.objects.get(id=author_id)
    #调用日志查看每次修改的的作者名
    #不同级别的我们可以调用不同的处理
    logger.info(author.name)
    # logger.error(author.name)
    # logger.warning(author.name)


    #如果是ｐｏｓｔ请求
    if request.method == "POST":
        #获取ｆｏｒ表单提交的信息
        new_author_name = request.POST.get("author_name")
        new_author_age = request.POST.get("author_age")
        new_book_name = request.POST.getlist("book_name")
        logger.critical(new_book_name)
        #　更新表单的提交数据
        author.name = new_author_name
        author.age = new_author_age
        author.save()
        #给第三张表添加外键
        author.book.set(new_book_name)
        return redirect('/book/author_list/')
    return render(request, 'book/edit_author.html', {"press_list": press_list, "book_list": book_list, "author": author})


#test
import time
def template_test(request):
    l = [11, 22, 33]
    d = {"name": "alex"}

    class Person(object):
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def dream(self):
            return "{} is dream...".format(self.name)

    Alex = Person(name="Alex", age=34)
    Egon = Person(name="Egon", age=9000)
    无言 = Person(name="无言", age=18)


    person_list = [Alex, Egon, 无言]
    mytime = 'lei wen  xuan'
    value2 = "<a href='#'>点我</a>"

    return render(request, "html/template_test.html", {'l': l, "person_list": person_list, 'web_time': "2018-11-01 9:20:00"})

def birthday(request):
    ret = book.objects.all()
    press_ret = Press.objects.all()
    birth = ''
    if request.method == "POST":
        birth = request.POST.get('birthday')
        print(birth)

    return render(request, 'book/book_list.html', {'birthday': birth, "book_list": ret, "press_list": press_ret})

