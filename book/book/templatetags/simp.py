from django import template

register = template.Library()


@register.simple_tag(name='add_list')
def simp(a, b, c):
   return a + b + c

@register.inclusion_tag(filename='html/test.html', name='page')
def my_page(num):
    data = [i for i in range(1, num+1)]
    return {"data": data}


if __name__ == '__main__':
    ret = simp(1,2,3)
    print(ret)
