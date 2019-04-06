from django.db import models


class Permission(models.Model):
    """
    权限
    """
    title = models.CharField(max_length=32, verbose_name='名称')
    url = models.CharField(max_length=32, verbose_name='URL')
    is_menu = models.BooleanField(default=False, verbose_name='是否是菜单')
    icon = models.CharField(max_length=32, blank=True, null=True, verbose_name='菜单图标')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限'


class Role(models.Model):
    """
    角色
    """
    name = models.CharField(max_length=32, verbose_name='角色名称')
    permissions = models.ManyToManyField('Permission', verbose_name='角色权限')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'


class User(models.Model):
    """
    用户
    """
    name = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    roles = models.ManyToManyField('Role', verbose_name='用户角色')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
