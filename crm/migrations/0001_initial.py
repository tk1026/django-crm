# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-03-15 12:56
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('mobile', models.CharField(blank=True, default=None, max_length=32, null=True, verbose_name='手机')),
                ('memo', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name_plural': '账户',
                'verbose_name': '账户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=64, verbose_name='客户名称')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='电话')),
                ('site', models.CharField(blank=True, max_length=128, null=True, verbose_name='客户所在地')),
                ('website', models.CharField(blank=True, max_length=32, null=True, verbose_name='网站')),
                ('account_type', models.CharField(blank=True, choices=[('supplier', '供应商'), ('dealer', '经销商'), ('distributor', '分销商'), ('other', '其它')], default=None, max_length=32, null=True, verbose_name='客户类型')),
                ('owner_ship', models.CharField(blank=True, choices=[('private', '私有'), ('public', '公开'), ('Gov', '政府'), ('subsidiary', '子公司'), ('other', '其它')], default=None, max_length=32, null=True, verbose_name='公司所有权')),
                ('industry', models.CharField(blank=True, choices=[('OEM', 'OEM'), ('App Server', '应用服务商'), ('ERP', '企业资源管理'), ('Gov', '政府'), ('Big', '大企业'), ('Small', '中小企业')], default=None, max_length=128, null=True, verbose_name='行业')),
                ('num', models.IntegerField(blank=True, null=True, verbose_name='员工数')),
                ('annual_revenue', models.IntegerField(blank=True, null=True, verbose_name='年收入')),
                ('address', models.CharField(blank=True, max_length=512, null=True, verbose_name='详细地址')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='客户拥有者')),
            ],
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=128, verbose_name='主题')),
                ('call_purpose', models.CharField(blank=True, choices=[('1', '调研'), ('2', '行政'), ('3', '谈判'), ('4', '演示'), ('5', '项目')], max_length=16, null=True, verbose_name='通话目的')),
                ('content', models.TextField(verbose_name='通话内容')),
            ],
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, choices=[('ad', '广告'), ('telephone', '推销电话'), ('introduction', '员工介绍'), ('medium', '公开媒介'), ('email', '销售邮件')], default=None, max_length=64, null=True, verbose_name='线索来源')),
                ('name', models.CharField(max_length=32, verbose_name='联系人名称')),
                ('email', models.CharField(blank=True, max_length=64, null=True, verbose_name='邮箱')),
                ('department', models.CharField(blank=True, max_length=32, null=True, verbose_name='部门')),
                ('designation', models.CharField(blank=True, max_length=32, null=True, verbose_name='职位')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='电话')),
                ('cellphone', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机')),
                ('birthday', models.DateField(blank=True, help_text='格式yyyy-mm-dd', null=True, verbose_name='出生日期')),
                ('address', models.CharField(blank=True, max_length=512, null=True, verbose_name='详细地址')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('account_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Accounts', verbose_name='客户名称')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='联系人所有者')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='部门名称')),
                ('count', models.IntegerField(default=0, verbose_name='人数')),
            ],
            options={
                'verbose_name_plural': '部门',
                'verbose_name': '部门',
            },
        ),
        migrations.CreateModel(
            name='Leads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=128, verbose_name='公司名称')),
                ('contact_name', models.CharField(max_length=32, verbose_name='联系人名称')),
                ('designation', models.CharField(blank=True, max_length=32, null=True, verbose_name='职位')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='电话')),
                ('cellphone', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机')),
                ('email', models.CharField(blank=True, max_length=64, null=True, verbose_name='邮箱')),
                ('website', models.CharField(blank=True, max_length=32, null=True, verbose_name='网站')),
                ('source', models.CharField(blank=True, choices=[('ad', '广告'), ('telephone', '推销电话'), ('introduction', '员工介绍'), ('medium', '公开媒介'), ('email', '销售邮件')], default=None, max_length=64, null=True, verbose_name='线索来源')),
                ('state', models.CharField(blank=True, choices=[('try', '尝试联系'), ('future', '将来联系'), ('contacted', '已联系'), ('uncontacted', '未联系'), ('false', '虚假线索'), ('lose', '丢失线索')], default=None, max_length=64, null=True, verbose_name='线索状态')),
                ('industry', models.CharField(blank=True, choices=[('OEM', 'OEM'), ('App Server', '应用服务商'), ('ERP', '企业资源管理'), ('Gov', '政府'), ('Big', '大企业'), ('Small', '中小企业')], default=None, max_length=128, null=True, verbose_name='行业')),
                ('num', models.IntegerField(blank=True, null=True, verbose_name='员工数')),
                ('annual_revenue', models.IntegerField(blank=True, null=True, verbose_name='年收入')),
                ('address', models.CharField(blank=True, max_length=512, null=True, verbose_name='详细地址')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='线索拥有者')),
            ],
        ),
        migrations.CreateModel(
            name='Potentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField(blank=True, null=True, verbose_name='金额')),
                ('name', models.CharField(max_length=128, verbose_name='商机名称')),
                ('closing_date', models.DateField(verbose_name='预计成交日期')),
                ('stage', models.CharField(choices=[('1', '需求分析'), ('2', '价值建议'), ('3', '确定决策者'), ('4', '提案/报价'), ('5', '谈判'), ('6', '成交')], max_length=16, verbose_name='阶段')),
                ('probability', models.CharField(blank=True, max_length=32, null=True, verbose_name='可能性')),
                ('next_step', models.CharField(blank=True, max_length=128, null=True, verbose_name='下一步')),
                ('source', models.CharField(blank=True, choices=[('ad', '广告'), ('telephone', '推销电话'), ('introduction', '员工介绍'), ('medium', '公开媒介'), ('email', '销售邮件')], default=None, max_length=64, null=True, verbose_name='线索来源')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('account_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Accounts', verbose_name='客户名称')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Contacts', verbose_name='联系人')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='商机拥有者')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=128, verbose_name='主题')),
                ('update', models.DateField(blank=True, null=True, verbose_name='到期日期')),
                ('status', models.CharField(blank=True, choices=[('1', '未启动'), ('2', '推迟'), ('3', '进行中'), ('4', '完成')], max_length=16, null=True, verbose_name='状态')),
                ('priority', models.CharField(blank=True, choices=[('high', '高'), ('highest', '最高'), ('low', '低'), ('lowest', '最低'), ('middle', '常规')], max_length=16, null=True, verbose_name='优先级')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Accounts', verbose_name='客户')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Contacts', verbose_name='联系人')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='任务所有者')),
            ],
        ),
        migrations.AddField(
            model_name='call',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Contacts', verbose_name='联系人'),
        ),
        migrations.AddField(
            model_name='call',
            name='related_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Accounts', verbose_name='关联到'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Department'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]