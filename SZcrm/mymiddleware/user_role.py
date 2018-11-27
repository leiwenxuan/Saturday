from django.utils.deprecation import MiddlewareMixin
from SZcrm import settings
from django.shortcuts import redirect, HttpResponse
import re
from django.urls import reverse


class UserPermission(MiddlewareMixin):
    def process_request(self, request):
        # 先获得白名单
        witer_url = getattr(settings, 'WHITE_URLS', [])
        new_url = request.path_info
        print(new_url, witer_url)
        for url in witer_url:
            if re.match(r'^{}$'.format(url), new_url):
                return None

        # 从session 获取url名单
        key = getattr(settings,'PERMISSION_SESSION_KEY', 'permission_url')
        auth_url = request.session.get(key, [])
        for url in auth_url:
            if re.match(r'^{}$'.format(url), new_url):
                return None
            return HttpResponse("你没有权限")
