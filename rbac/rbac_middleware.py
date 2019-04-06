#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 7:32 PM
# @Author  : Tkungen
# @File    : rbac_middleware.py
# @Software: PyCharm
import re
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class Permission(MiddlewareMixin):
    def process_request(self, request):
        # 当前访问url
        current_url = request.path_info
        # 白名单
        for item in settings.WHITE_LIST:
            if re.match(item, current_url):
                return

        # 读取用户权限
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        for item in permission_list:
            url = item['url']
            if re.match(url, current_url):
                return
        else:
            return HttpResponse('无权访问！')
