'''
    设置session　数据
'''
from SZcrm import settings
def init(request, user_obj):
    # 1.查询用户权限
    # 2.把查询的url 添加到session 里面
    url_list = user_obj.roles.all().values(
        'permissions__url', 'permissions__title',
        'permissions__is_menu', 'permissions__icon'
    ).distinct()  # 返回的QuerySet对象，没个元素都是元组
    # 3.把查询的ｕｒｌ加入列表
    print(url_list)
    print('-3-' * 12)
    # 取到url_list
    #  permissions_list = [permissions['permissions__url'] for permissions in url_list]
    permissions_list = []
    # 存放菜单列表
    menu_list = []
    for i in url_list:
        permissions_list.append(i['permissions__url'])
        if i.get('permissions__is_menu'):
            menu_list.append(
                {
                    'url': i['permissions__url'],
                    'title': i['permissions__title'],
                    'icon': i['permissions__icon'],
                }
            )
    print('url', permissions_list)
    print('菜单', menu_list)
    session_key = getattr(settings, 'PERMISSION_URL_KEY',
                          'permissions_url')
    menu_key = getattr(settings, 'SECRET_MENU', 'menu_list')

    # 设置session, 存取menu列表
    request.session[menu_key] = menu_list
    # 设置session, 存取ｕｒｌ列表
    request.session[session_key] = permissions_list
