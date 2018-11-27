from django.utils.deprecation import MiddlewareMixin
from SZcrm import settings
from django.shortcuts import HttpResponse, redirect
import re


class LoginMiddle(MiddlewareMixin):
    def process_request(self, request):
        # 1. 获取白名单，　没有找到为[]
        white_list = getattr(settings, 'WHITE_URLS', [])
        # 2. 获取当前的url
        new_url = request.path_info
        print(new_url, 'what are you?')
        print(white_list)
        for url in white_list:
            if re.match(r'^{}$'.format(url), new_url):
                return None
        # 2. 获取session的里面设置url
        session_key = getattr(settings, 'PERMISSION_URL_KEY',
                              'permissions_url')
        for url in request.session.get(session_key, []):
            print(url)
            if re.match(r'^{}$'.format(url), new_url):
                return
        else:
            return HttpResponse("没有此权限")
