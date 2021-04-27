from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import SafeData, SafeString, mark_safe

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    Phone = models.CharField(blank=True, max_length=20)
    Address = models.CharField(blank=True, max_length=200)
    City = models.CharField(blank=True, max_length=20)
    Country = models.CharField(blank=True, max_length=20)
    Image = models.ImageField(blank=True, upload_to='images/user/')

    def __str__(self):
        return self.User.first_name

    def username(self):
        return self.user.first_name+' '+self.user.last_name+' '+'['+self.user.username+']'

    def image_tag(self):
        if self.Image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.Image.url))
        else:
            return ""

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
