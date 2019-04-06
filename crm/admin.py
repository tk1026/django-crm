from django.contrib import admin
from crm import models
# Register your models here.

class LeadsAdmin(admin.ModelAdmin):
    list_filter = ('company', 'contact_name', 'source')



admin.site.register(models.Accounts)
admin.site.register(models.Contacts)
admin.site.register(models.UserProfile)
admin.site.register(models.Department)
admin.site.register(models.Call)
admin.site.register(models.Leads, LeadsAdmin)
admin.site.register(models.Potentials)
admin.site.register(models.Tasks)
