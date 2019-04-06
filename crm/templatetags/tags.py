#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/26 10:00 PM
# @Author  : Tkungen
# @File    : tags.py
# @Software: PyCharm

from django import template

register = template.Library()


@register.simple_tag
def get_stage_bg(potential_obj):
    bg = ''
    if potential_obj.stage == '10%' or potential_obj.stage == '25%':
        bg = 'bg-success'
    elif potential_obj.stage == '50%':
        bg = 'bg-info'
    elif potential_obj.stage == '75%':
        bg = 'bg-warning'
    elif potential_obj.stage == '100%':
        bg = 'bg-danger'
    return bg
