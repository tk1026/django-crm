#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/4/4 5:53 PM
# @Author  : Tkungen
# @File    : init_permission.py
# @Software: PyCharm
from django.conf import settings


def init_permission(user, request):
    permissions = []
    # 存放权限菜单
    menus = []
    # 查询用户权限
    permission_list = user.roles.filter(permissions__url__isnull=False).values('permissions__url',
                                                                               'permissions__is_menu',
                                                                               'permissions__title',
                                                                               'permissions__icon')
    for item in permission_list:
        # 构造权限url列表
        permissions.append({'url': item['permissions__url']})
        # 构造权限菜单列表
        if item['permissions__is_menu']:
            menus.append({
                'url': item['permissions__url'],
                'title': item['permissions__title'],
                'icon': item['permissions__icon']
            })

    # 将当前用户权限url和权限菜单写入session
    request.session[settings.PERMISSION_SESSION_KEY] = permissions
    request.session[settings.MENU_SESSION_KEY] = menus
