#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 7:48 PM
# @Author  : Tkungen
# @File    : forms.py
# @Software: PyCharm
from django import forms
from django.core.exceptions import ValidationError
from crm import models


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():  # 修改全体样式
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', required=True, min_length=4,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               error_messages={
                                   'required': '请输入用户名',
                                   'min_length': '用户名最少4个字符'
                               })
    password = forms.CharField(label='密码', required=True, min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               error_messages={
                                   'required': '请输入密码',
                                   'min_length': '密码最少6个字符'
                               })


class RegisterForm(BaseForm):
    re_password = forms.CharField(
        label='确认密码',
        required=True,
        widget=forms.widgets.PasswordInput(),
        error_messages={'required': '确认密码不能为空'}
    )

    class Meta:
        model = models.UserProfile
        fields = ['username', 'password', 're_password', 'name']
        widgets = {
            'password': forms.widgets.PasswordInput()
        }
        labels = {
            'username': '用户名',
            'password': '密码',
            'name': '员工姓名'
        }
        error_messages = {
            'password': {
                'required': '密码不能为空'
            }
        }

    # 自定义验证相互依赖的字段
    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd == re_pwd:
            return self.cleaned_data
        self.add_error('re_password', '两次密码不一致')
        raise ValidationError('两次密码不一致')


class LeadsForm(BaseForm):
    class Meta:
        model = models.Leads
        fields = '__all__'


class ContactsForm(BaseForm):
    class Meta:
        model = models.Contacts
        fields = '__all__'


class AccountsForm(BaseForm):
    class Meta:
        model = models.Accounts
        fields = '__all__'


class TasksForm(BaseForm):
    class Meta:
        model = models.Tasks
        fields = '__all__'


class CallForm(BaseForm):
    class Meta:
        model = models.Call
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leads'].widget.choices = [(self.instance.leads_id, self.instance.leads), ]


class CallContactForm(CallForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact'].widget.choices = [(self.instance.contact_id, self.instance.contact), ]


class CallAccountForm(CallForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_to'].widget.choices = [(self.instance.related_to_id, self.instance.related_to), ]


class PotentialsForm(BaseForm):
    class Meta:
        model = models.Potentials
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_name'].widget.choices = [(self.instance.account_name_id, self.instance.account_name), ]
