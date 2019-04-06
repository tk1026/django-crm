from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.db.models import Q
from django.contrib import auth

from crm import models
from crm import forms
from utils.pagination import Pagination
from rbac.init_permission import init_permission


def login(request):
    err_msg = ''
    form_obj = forms.LoginForm()
    if request.method == 'POST':
        form_obj = forms.LoginForm(request.POST)
        if form_obj.is_valid():
            username = form_obj.cleaned_data['username']
            password = form_obj.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)

                init_permission(user, request)
                return redirect('index')

            err_msg = '用户名或密码错误'

    return render(request, 'login.html', locals())


def logout_view(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    form_obj = forms.RegisterForm()
    if request.method == 'POST':
        form_obj = forms.RegisterForm(request.POST)
        if form_obj.is_valid():
            obj = form_obj.save()
            obj.set_password(obj.password)
            obj.save()

            return redirect('login')

    return render(request, 'register.html', locals())


def index(request):
    leads = models.Leads.objects.filter(owner=request.user).count()
    accounts = models.Accounts.objects.filter(owner=request.user).count()
    potentials = models.Potentials.objects.filter(owner=request.user).count()
    to_do_list = models.Tasks.objects.filter(owner=request.user)

    return render(request, 'index.html', locals())


# 线索展示
class LeadsView(View):
    def get(self, request):
        filter_fields = ['company', 'contact_name', 'source']
        search_conditions = self.get_search_conditions(filter_fields)

        all_leads = models.Leads.objects.filter(search_conditions)
        page = Pagination(request, all_leads.count(), per_num=2, query_params=request.GET)

        return render(request, 'leads_list.html', {
            'all_leads': all_leads[page.get_slice_start:page.get_slice_end],
            'page_li': page.show_li()
        })

    def post(self, request):
        action = self.request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        getattr(self, action)()

        return self.get(request)

    def multi_del(self):
        ids = self.request.POST.getlist('ids')
        models.Leads.objects.filter(id__in=ids).delete()

    # 转换线索为客户
    def transform(self):
        ids = self.request.POST.getlist('ids')
        leads_obj_list = models.Leads.objects.filter(id__in=ids)
        accounts_obj_list = []
        contacts_obj_list = []
        for leads_obj in leads_obj_list:
            accounts_obj_list.append(
                models.Accounts(owner=leads_obj.owner, company=leads_obj.company, phone=leads_obj.phone,
                                website=leads_obj.website, industry=leads_obj.industry, num=leads_obj.num,
                                annual_revenue=leads_obj.annual_revenue, address=leads_obj.address))

            contacts_obj_list.append(
                models.Contacts(owner=leads_obj.owner, source=leads_obj.source, name=leads_obj.contact_name,
                                email=leads_obj.email, designation=leads_obj.designation,
                                phone=leads_obj.phone, cellphone=leads_obj.cellphone, address=leads_obj.address))

        models.Accounts.objects.bulk_create(accounts_obj_list)
        models.Contacts.objects.bulk_create(contacts_obj_list)
        leads_obj_list.delete()

    # 搜索条件
    def get_search_conditions(self, filter_fields):
        """
        :param filter_fields: 待过滤字段
        :return:Q对象
        """
        # 获取搜索关键词
        search_key = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for filter_field in filter_fields:
            q.children.append(('{}__contains'.format(filter_field), search_key))
        return q


# 展示线索详细信息
def detail_leads(request, id):
    # 该线索对象
    leads_obj = models.Leads.objects.filter(id=id).first()
    # 查找该模型对象的任务对象列表
    tasks_obj_list = models.Tasks.objects.filter(leads=leads_obj)
    # 通话
    call_obj_list = models.Call.objects.filter(leads=leads_obj)
    obj = models.Call(leads=leads_obj)
    form_obj = forms.CallForm(instance=obj)
    if request.method == 'POST':
        form_obj = forms.CallForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
    return render(request, 'leads_detail.html', locals())


# 编辑任务
def leads_tasks_edit(request, obj_id):
    tasks_obj = models.Tasks.objects.filter(id=obj_id).first()
    form_obj = forms.TasksForm(instance=tasks_obj)
    if request.method == 'POST':
        form_obj = forms.TasksForm(request.POST, instance=tasks_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('detail_leads')
    return render(request, 'tasks_detail.html', locals())


# 新增线索
def create_leads(request):
    form_obj = forms.LeadsForm()
    if request.method == 'POST':
        form_obj = forms.LeadsForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('leads')
    return render(request, 'leads_create.html', locals())


# 编辑线索
def edit_leads(request, edit_id):
    edit_obj = models.Leads.objects.filter(id=edit_id).first()
    form_obj = forms.LeadsForm(instance=edit_obj)
    if request.method == 'POST':
        form_obj = forms.LeadsForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('leads')
    return render(request, 'leads_edit.html', locals())


# 联系人列表
def contacts_list(request):
    all_contacts = models.Contacts.objects.all()
    page = Pagination(request, all_contacts.count(), per_num=3, query_params=request.GET)
    return render(request, 'contacts_list.html', {
        'all_contacts': all_contacts[page.get_slice_start:page.get_slice_end],
        'page_li': page.show_li()
    })


# 展示联系人详细信息
def detail_contacts(request, id):
    # 该线索对象
    contact_obj = models.Leads.objects.filter(id=id).first()
    # 查找该模型对象的任务对象列表
    tasks_obj_list = models.Tasks.objects.filter(contact=contact_obj)
    # 通话
    call_obj_list = models.Call.objects.filter(contact=contact_obj)
    call_obj = models.Call(contact=contact_obj)
    form_obj = forms.CallContactForm(instance=call_obj)
    if request.method == 'POST':
        form_obj = forms.CallForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
    return render(request, 'contacts_detail.html', locals())


# 增加/编辑联系人
def contacts(request, edit_id=None):
    edit_obj = models.Contacts.objects.filter(id=edit_id).first()
    form_obj = forms.ContactsForm(instance=edit_obj)
    if request.method == 'POST':
        form_obj = forms.ContactsForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('contacts_list')
    return render(request, 'contacts_create_edit.html', {'form_obj': form_obj, 'edit_id': edit_id})


# 客户列表
def accounts_list(request):
    all_accounts = models.Accounts.objects.all()
    page = Pagination(request, all_accounts.count(), per_num=3, query_params=request.GET)
    return render(request, 'accounts_list.html', {
        'all_accounts': all_accounts[page.get_slice_start:page.get_slice_end],
        'page_li': page.show_li()
    })


# 增加/编辑客户
def accounts(request, edit_id=None):
    edit_obj = models.Accounts.objects.filter(id=edit_id).first()
    form_obj = forms.AccountsForm(instance=edit_obj)
    if request.method == 'POST':
        form_obj = forms.AccountsForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('accounts_list')
    return render(request, 'accounts_create_edit.html', {'form_obj': form_obj, 'edit_id': edit_id})


# 展示客户详细信息
def detail_accounts(request, id):
    # 该客户对象
    account_obj = models.Accounts.objects.filter(id=id).first()
    potentials_list = models.Potentials.objects.filter(account_name=account_obj)
    # 查找该模型对象的任务对象列表
    tasks_obj_list = models.Tasks.objects.filter(account=account_obj)
    # 通话
    call_obj_list = models.Call.objects.filter(related_to=account_obj)
    form_obj = forms.CallForm()
    if request.method == 'POST':
        form_obj = forms.CallForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()

    # 商机
    potential_obj = models.Potentials.objects.filter(account_name=account_obj).first()
    obj = models.Potentials(account_name=account_obj)
    potentials_form = forms.PotentialsForm(instance=obj)
    if request.method == 'POST':
        potentials_form = forms.PotentialsForm(request.POST)
        if potentials_form.is_valid():
            potentials_form.save()

    # 获取通话内容
    call_re = request.GET.get('call_record', )
    # 将数据添加到数据库
    if (not call_re == '') and (not call_re == None):
        models.Call.objects.create(content=call_re, related_to=account_obj)
    return render(request, 'accounts_detail.html', locals())


# 商机列表
class PotentialsView(View):
    def get(self, request):
        filter_fields = ['name']
        search_conditions = self.get_search_conditions(filter_fields)

        all_potentials = models.Potentials.objects.filter(search_conditions)
        page = Pagination(request, all_potentials.count(), per_num=2, query_params=request.GET)

        return render(request, 'potentials_list.html', {
            'all_potentials': all_potentials[page.get_slice_start:page.get_slice_end],
            'page_li': page.show_li()
        })

    def post(self, request):
        action = self.request.POST.get('action')
        if not hasattr(self, action):
            return HttpResponse('非法操作')
        getattr(self, action)()

        return self.get(request)

    def multi_del(self):
        ids = self.request.POST.getlist('ids')
        obj = models.Potentials.objects.filter(id__in=ids)
        print(obj)

    # 搜索条件
    def get_search_conditions(self, filter_fields):
        """
        :param filter_fields: 待过滤字段
        :return:Q对象
        """
        # 获取搜索关键词
        search_key = self.request.GET.get('query', '')
        q = Q()
        q.connector = 'OR'
        for filter_field in filter_fields:
            q.children.append(('{}__contains'.format(filter_field), search_key))
        return q


# 增加/编辑商机
def potentials(request, edit_id=None):
    edit_obj = models.Potentials.objects.filter(id=edit_id).first()
    form_obj = forms.PotentialsForm(instance=edit_obj)
    if request.method == 'POST':
        form_obj = forms.PotentialsForm(request.POST, instance=edit_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('potentials_list')
    return render(request, 'potentials_create_edit.html', {'form_obj': form_obj, 'edit_id': edit_id})


# 商机详细信息
def detail_potentials(request, id):
    potential_obj = models.Potentials.objects.filter(id=id).first()
    return render(request, 'potentials_detail.html', locals())
