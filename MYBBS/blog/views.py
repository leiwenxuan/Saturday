from django.shortcuts import render, HttpResponse
from blog import models

# Create your views here.

def pwd(request):
    return render(request, 'pwd.html')

# 主页
def index(request):
    article_obj = models.Article.objects.all()

    seed_data = {
        'article_obj': article_obj,
    }
    return render(request, 'index.html', seed_data)


# 我的主页
def home(request):
    article_obj = models.Article.objects.all()

    seed_data = {
        'article_obj': article_obj,
    }
    return render(request, 'index.html', seed_data)




