from django import template
from SZcrm import settings
import re
register = template.Library()


@register.inclusion_tag(filename='rbac/menu.html')
def meun_list(request):
    new_url = request.path_info
    meun_key = getattr(settings, 'SECRET_MENU', 'menu_list')
    meun_list = request.session.get(meun_key)
    for meun in meun_list:
        if re.match(r'^{}$'.format(meun['url']), new_url):
            meun['class'] = 'active'
    return {'menu_list': meun_list}
