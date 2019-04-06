from django.db import models
from django.contrib.auth.models import AbstractUser

from rbac.models import Role

# Create your models here.

source_choices = (
    ('ad', '广告'),
    ('telephone', '推销电话'),
    ('introduction', '员工介绍'),
    ('medium', '公开媒介'),
    ('email', '销售邮件'),
)

status_choices = (
    ('try', '尝试联系'),
    ('future', '将来联系'),
    ('contacted', '已联系'),
    ('uncontacted', '未联系'),
    ('false', '虚假线索'),
    ('lose', '丢失线索'),
)

industry_choices = (
    ('OEM', 'OEM'),
    ('App Server', '应用服务商'),
    ('ERP', '企业资源管理'),
    ('Gov', '政府'),
    ('Big', '大企业'),
    ('Small', '中小企业'),
)

stage_choices = (
    ('10%', '需求分析'),
    ('25%', '价值建议'),
    ('50%', '确定决策者'),
    ('75%', '提案/报价'),
    ('100%', '成交'),
)

type_choices = (
    ('supplier', '供应商'),
    ('dealer', '经销商'),
    ('distributor', '分销商'),
    ('other', '其它'),
)

ownership_choices = (
    ('private', '私有'),
    ('public', '公开'),
    ('Gov', '政府'),
    ('subsidiary', '子公司'),
    ('other', '其它'),
)

tasks_status_choices = (
    ('1', '未启动'),
    ('2', '推迟'),
    ('3', '进行中'),
    ('4', '完成'),
)

priority_choices = (
    ('high', '高'),
    ('highest', '最高'),
    ('low', '低'),
    ('lowest', '最低'),
    ('middle', '常规'),
)

call_purpose_choices = (
    ('1', '调研'),
    ('2', '行政'),
    ('3', '谈判'),
    ('4', '演示'),
    ('5', '项目'),
)


class Tasks(models.Model):
    """
    任务
    """
    owner = models.ForeignKey('UserProfile', verbose_name='任务所有者')
    subject = models.CharField(max_length=128, verbose_name='主题')
    update = models.DateField(blank=True, null=True, verbose_name='到期日期')
    contact = models.ForeignKey('Contacts', blank=True, null=True, verbose_name='联系人')
    account = models.ForeignKey('Accounts', blank=True, null=True, verbose_name='客户')
    leads = models.ForeignKey('Leads', blank=True, null=True, verbose_name='线索')
    status = models.CharField(max_length=16, choices=tasks_status_choices, blank=True, null=True, verbose_name='状态')
    priority = models.CharField(max_length=16, choices=priority_choices, blank=True, null=True, verbose_name='优先级')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'


class Call(models.Model):
    """
    通话
    """
    contact = models.ForeignKey('Contacts', blank=True, null=True, verbose_name='联系人')
    subject = models.CharField(max_length=128, verbose_name='主题')
    call_purpose = models.CharField(max_length=16, choices=call_purpose_choices, blank=True, null=True,
                                    verbose_name='通话目的')
    related_to = models.ForeignKey('Accounts', blank=True, null=True, verbose_name='关联到')
    leads = models.ForeignKey('Leads', blank=True, null=True, verbose_name='线索')
    content = models.TextField(verbose_name='通话内容')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = '通话'
        verbose_name_plural = '通话'


class Contacts(models.Model):
    """
    联系人
    """
    owner = models.ForeignKey('UserProfile', verbose_name='联系人所有者')
    source = models.CharField(choices=source_choices, max_length=64, default=None, blank=True, null=True,
                              verbose_name='线索来源')
    name = models.CharField(max_length=32, verbose_name='联系人名称')
    account_name = models.ForeignKey('Accounts', blank=True, null=True, verbose_name='客户名称')
    email = models.CharField(max_length=64, blank=True, null=True, verbose_name='邮箱')
    department = models.CharField(max_length=32, blank=True, null=True, verbose_name='部门')
    designation = models.CharField(max_length=32, blank=True, null=True, verbose_name='职位')
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='电话')
    cellphone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机')
    birthday = models.DateField('出生日期', help_text="格式yyyy-mm-dd", blank=True, null=True)
    address = models.CharField(max_length=512, blank=True, null=True, verbose_name='详细地址')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = '联系人'


class Accounts(models.Model):
    """
    客户表
    """
    owner = models.ForeignKey('UserProfile', verbose_name='客户拥有者')
    company = models.CharField(max_length=64, verbose_name='客户名称')
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='电话')
    site = models.CharField(max_length=128, blank=True, null=True, verbose_name='客户所在地')
    website = models.CharField(max_length=32, blank=True, null=True, verbose_name='网站')
    account_type = models.CharField(choices=type_choices, max_length=32, default=None, blank=True, null=True,
                                    verbose_name='客户类型')
    owner_ship = models.CharField(choices=ownership_choices, max_length=32, default=None, blank=True, null=True,
                                  verbose_name='公司所有权')

    industry = models.CharField(choices=industry_choices, max_length=128, default=None, blank=True, null=True,
                                verbose_name='行业')
    num = models.IntegerField(blank=True, null=True, verbose_name='员工数')
    annual_revenue = models.IntegerField(blank=True, null=True, verbose_name='年收入')
    address = models.CharField(max_length=512, blank=True, null=True, verbose_name='详细地址')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'


class Leads(models.Model):
    """
    线索表
    """
    owner = models.ForeignKey('UserProfile', verbose_name='线索拥有者')
    company = models.CharField(max_length=128, verbose_name='公司名称')
    contact_name = models.CharField(max_length=32, verbose_name='联系人名称')
    designation = models.CharField(max_length=32, blank=True, null=True, verbose_name='职位')
    phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='电话')
    cellphone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机')
    email = models.CharField(max_length=64, blank=True, null=True, verbose_name='邮箱')
    website = models.CharField(max_length=32, blank=True, null=True, verbose_name='网站')
    source = models.CharField(choices=source_choices, max_length=64, default=None, blank=True, null=True,
                              verbose_name='线索来源')
    state = models.CharField(choices=status_choices, max_length=64, default=None, blank=True, null=True,
                             verbose_name='线索状态')
    industry = models.CharField(choices=industry_choices, max_length=128, default=None, blank=True, null=True,
                                verbose_name='行业')
    num = models.IntegerField(blank=True, null=True, verbose_name='员工数')
    annual_revenue = models.IntegerField(blank=True, null=True, verbose_name='年收入')
    address = models.CharField(max_length=512, blank=True, null=True, verbose_name='详细地址')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = '线索'
        verbose_name_plural = '线索'


class Potentials(models.Model):
    """
    商机表
    """
    owner = models.ForeignKey('UserProfile', verbose_name='商机拥有者')
    money = models.IntegerField(blank=True, null=True, verbose_name='金额')
    name = models.CharField(max_length=128, verbose_name='商机名称')
    closing_date = models.DateField(verbose_name='预计成交日期')
    account_name = models.ForeignKey('Accounts', verbose_name='客户名称')
    stage = models.CharField(max_length=16, choices=stage_choices, verbose_name='阶段')
    probability = models.CharField(max_length=32, blank=True, null=True, verbose_name='可能性')
    next_step = models.CharField(max_length=128, blank=True, null=True, verbose_name='下一步')
    source = models.CharField(choices=source_choices, max_length=64, default=None, blank=True, null=True,
                              verbose_name='线索来源')
    contact = models.ForeignKey('Contacts', blank=True, null=True, verbose_name='联系人')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商机'
        verbose_name_plural = '商机'


class Department(models.Model):
    """
    部门表
    """
    name = models.CharField(max_length=32, verbose_name='部门名称')
    count = models.IntegerField(default=0, verbose_name='人数')

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'


class UserProfile(AbstractUser):
    """
    账户表
    """
    name = models.CharField('姓名', max_length=32)
    mobile = models.CharField('手机', max_length=32, default=None, blank=True, null=True)
    memo = models.TextField('备注', default=None, blank=True, null=True)
    department = models.ForeignKey('Department', default=None, blank=True, null=True)
    roles = models.ManyToManyField(Role, verbose_name='用户角色')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '账户'
        verbose_name_plural = '账户'
