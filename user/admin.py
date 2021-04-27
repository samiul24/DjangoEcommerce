from django.contrib import admin
from user.models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username','Phone','Address','City','Country','image_tag']

admin.site.register(UserProfile,UserProfileAdmin)
