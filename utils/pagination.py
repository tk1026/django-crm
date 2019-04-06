#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/20 5:01 PM
# @Author  : Tkungen
# @File    : pagination.py
# @Software: PyCharm
from django.utils.safestring import mark_safe
from django.http import QueryDict


class Pagination:

    def __init__(self, request, all_count=308, per_num=10, max_show=11, query_params=QueryDict()):
        self.request = request
        self.url = self.request.path_info
        self.all_count = all_count  # 总数据数
        self.per_num = per_num  # 每页显示数据条数
        self.max_show = max_show  # 最多显示页码数
        self.half_show = max_show // 2
        self.query_params = query_params  # 查询参数

    @property
    def total_num(self):
        # 总页码数
        total_num, more = divmod(self.all_count, self.per_num)
        if more:  # 如果有余数则总页码数加一
            total_num += 1
        return total_num

    @property
    def current_page(self):
        # 当前页面
        try:
            current_page = int(self.request.GET.get('page', 1))
            # 如果当前页面大于总页面，总页面刚好为0，则再将当前页面赋值为1
            if current_page >= self.total_num:
                current_page = self.total_num
            if current_page <= 0:
                current_page = 1
        except:
            current_page = 1
        return current_page

    @property
    def page_start(self):
        # 当前页码页面的开始页面值
        page_start = self.current_page - self.half_show
        if page_start <= 0:
            page_start = 1
        return page_start

    @property
    def page_end(self):
        # 当前页码页面的结束页面值
        page_end = self.current_page + self.half_show
        if page_end > self.total_num:
            page_end = self.total_num
        return page_end

    def show_li(self):
        # 存放li标签
        html_list = []

        # 深度复制QueryDict，使其可修改
        params = self.query_params.copy()
        # 上一页search和pagination组合url
        params['page'] = self.current_page - 1

        # 上一页
        if self.current_page - 1 <= 0:
            prev_li = '<li class="paginate_button page-item previous disabled"><a class="page-link">Previous</a></li>'
        else:
            prev_li = '<li class="paginate_button page-item previous"><a class="page-link" href="{1}?{0}">Previous</a></li>'.format(
                params.urlencode(), self.url)
        html_list.append(prev_li)

        for num in range(self.page_start, self.page_end + 1):
            # 分页上search和pagination组合url
            params['page'] = num
            if self.current_page == num:
                li_html = '<li class="paginate_button page-item active"><a class="page-link" href="{0}?{1}">{2}</a></li>'.format(
                    self.url, params.urlencode(), num)
            else:
                li_html = '<li class="paginate_button page-item"><a class="page-link" href="{0}?{1}">{2}</a></li>'.format(
                    self.url, params.urlencode(), num)
            html_list.append(li_html)

        # 下一页search和pagination组合url
        params['page'] = self.current_page + 1

        # 下一页
        if self.current_page >= self.total_num:
            next_li = '<li class="paginate_button page-item next disabled"><a class="page-link">Next</a></li>'
        else:
            next_li = '<li class="paginate_button page-item next"><a class="page-link" href="{1}?{0}"><span>&raquo;</span></a></li>'.format(
                params.urlencode(), self.url)
        html_list.append(next_li)

        html_str = mark_safe(''.join(html_list))

        return html_str

    @property
    def get_slice_start(self):
        start = (self.current_page - 1) * self.per_num
        return start

    @property
    def get_slice_end(self):
        end = self.current_page * self.per_num
        return end
