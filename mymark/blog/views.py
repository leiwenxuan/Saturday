from django.shortcuts import render, HttpResponse
from blog import models
import markdown
from django import views
# Create your views here.

from blog.forms import add_form

def test_md(request):
    ret = models.ExampleModel.objects.get(name='md')

    ret.content = markdown.markdown(ret.content.replace("\r\n", '  \n'), extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ], safe_mode=True, enable_attributes=False)

    return render(request, 'test.html', {'content': ret})
def make(request):
    ret = models.ExampleModel.objects.get(name='无言')

    # ret.content = markdown.markdown(ret.content.replace("\r\n", '  \n'), extensions=[
    #     'markdown.extensions.extra',
    #     'markdown.extensions.codehilite',
    #     'markdown.extensions.toc',
    # ], safe_mode=True, enable_attributes=False)

    return render(request, 'make.html', {'post': ret})

class TestView(views.View):
    def get(self, request):
        ret = models.ExampleModel.objects.get(name='无言')

        ret.content = markdown.markdown(ret.content.replace("\r\n", '  \n'), extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ], safe_mode=True, enable_attributes=False)
        return render(request, 'login.html')
        # return render(request, 'test.html', {'content': ret})

    def post(self,request):
        # name = request.POST.get('username')
        print(request.POST)
        print( request.FILES)
        filename = request.FILES.get('filename')
        print(filename)
        print(filename.name)

        data = ''
        # with open(filename.name, 'wb') as f:
        #     # for i in filename:
        #     #     f.write(i)
        for i in filename:
            data += i.decode('utf-8')
        models.ExampleModel.objects.create(name='md', content=data)

        return HttpResponse("KO！")

def index(request):
    if request.method == 'POST':
        forms = add_form(request.POST)
        print(forms)
        return HttpResponse('KO')
    else:
        form = add_form()

    print('='*120)
    return render(request,'index.html', {"form": form})





