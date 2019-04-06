from django.contrib import admin
from rbac import models


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url', 'is_menu', 'icon']
    list_editable = ['title', 'url', 'icon']


admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.Permission, PermissionAdmin)
