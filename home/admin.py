from django.contrib import admin
from home.models import Setting,ContactMessage,FAQ

# Register your models here.
class SettingAdmin(admin.ModelAdmin):
    list_display = ['Title','Company','Update_at','Status',]
    list_filter = ['Company','Status', ]

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['Name','Subject','Message','Status']
    list_filter =  ['Status']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['Question','Answer','Status']
    list_filter =  ['Status']

admin.site.register(Setting,SettingAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
