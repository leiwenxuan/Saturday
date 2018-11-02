from django.shortcuts import render,HttpResponse
# Create your views here.
from .models import Article
from .models import Category, Banner, Tag, Link

#　欢迎页面
def hello(request):
    '''
    一个简单的欢迎页面
    :param request:
    :return:
    '''
    return HttpResponse("欢迎使用Ｄｊａｎｇｏ2")

# 测试函数

def index1(request):
    '''
    一个简单视图函数
    :param request:
    :return:
    '''
    # 添加两个变量
    sitename = '无言的博客'
    url = 'www.leiwenxuan.cn'
    #添加一个新列表
    list=[
        '开发前的准备',
        '项目需求分析',
        '数据库设计分析',
        '创建项目',
        '基础配置',
        '欢迎页面',
        '创建数据库模型',
    ]
    #　添加一个联系方式
    mydict = {
        'name': '无言',
        'qq': '892028617',
        'wx': '保密',
        'email': '892028617@qq.com',
    }

    #把变量封装上下文
    context = {
        'sitename': sitename,
        'url':url,
        'list': list,
        'mydict': mydict,
    }
    return render(request, 'index.html', context)


def index2(request):
    '''
    :param request:
    :return:
    '''
    # 对Article 进行声明实例化，　　然后生成对象 allarticle
    allarticle = Article.objects.all()

    # 把查询的对象封装到上下文
    context = {
        'allarticle': allarticle,
    }

    return render(request, 'index.html', context)


#首页
def index(request):
    #　从models 里导入Gategor
    allcategory = Category.objects.all().order_by('id')[0:10]

    tui = Article.objects.filter(tui__id=1)[:3] # 查询推荐为１的文章
    # hot = Article.objects.all().order_by('?')[:10]#随机推荐
    # hot = Article.objects.filter(tui_id=3)[:10]   #通过推荐进行查询，以推荐ID是3为例
    hot = Article.objects.all().order_by('views')[:10]  # 通过浏览数进行排序
    remen = Article.objects.filter(tui__id=2)[:6]
    tags = Tag.objects.all()
    link = Link.objects.all()

    context = {
        'allcategory': allcategory,
        'tui': tui,
        'hot': hot,
        'remen': remen,
        'tags': tags,
        'link': link,
    }
    return render(request, 'index.html', context)


#列表页
def list(request,lid):
    list = Article.objects.filter(category_id=lid)  # 获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid)  # 获取当前文章的栏目名
    remen = Article.objects.filter(tui__id=2)[:6]  # 右侧的热门推荐
    allcategory = Category.objects.all()  # 导航所有分类
    tags = Tag.objects.all()  # 右侧所有文章标签

    page = request.GET.get('page')  # 在URL中获取当前页面数
    paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'list.html', locals())

#内容页
def show(request,sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    allcategory = Category.objects.all()  # 导航上的分类
    tags = Tag.objects.all()  # 右侧所有标签
    remen = Article.objects.filter(tui__id=2)[:6]  # 右侧热门推荐
    hot = Article.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐
    previous_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    netx_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals())

#标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)  # 通过文章标签进行查询文章
    remen = Article.objects.filter(tui__id=2)[:6]
    allcategory = Category.objects.all()
    tname = Tag.objects.get(name=tag)  # 获取当前搜索的标签名
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'tags.html', locals())

# 搜索页
def search(request):
    ss = request.GET.get('search')  # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配
    remen = Article.objects.filter(tui__id=2)[:6]
    allcategory = Category.objects.all()
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())


# 关于我们
def about(request):
    allcategory = Category.objects.all()
    return render(request, 'page.html', locals())
