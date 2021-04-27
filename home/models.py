from django.db import models
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from product.models import Product


# Create your models here.
class Setting(models.Model):
    STATUS =(
        ('True', 'True'),
        ('False','False'),
    )
    Title = models.CharField(max_length=150)
    Keywords = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Company = models.CharField(max_length=50)
    Address = models.CharField(blank=True, max_length=100)
    Phone = models.CharField(blank=True, max_length=15)
    Fax = models.CharField(blank=True, max_length=100)
    Email = models.CharField(blank=True, max_length=50)
    Smtpserver = models.CharField(blank=True, max_length=50)
    Smtpmail = models.CharField(blank=True,max_length=50)
    Smtpport = models.CharField(blank=True,max_length=15)
    Icon = models.ImageField(blank=True,upload_to='images/')
    Facebook = models.CharField(blank=True, max_length=100)
    Instagram = models.CharField(blank=True,max_length=100)
    Twitter = models.CharField(blank=True,max_length=100)
    Youtube = models.CharField(blank=True,max_length=100)
    Aboutus = RichTextUploadingField(blank=True)
    Contact = RichTextUploadingField(blank=True)
    References = RichTextUploadingField(blank=True)
    Status = models.CharField(max_length=50, choices=STATUS)
    Create_at = models.DateTimeField(auto_now_add=True)
    Update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Title

class ContactMessage(models.Model):
    STATUS =(
        ('New','New'),
        ('Read','Read'),
        ('Closed','Closed'),
    )
    Name = models.CharField(blank=True,max_length=100)
    Email = models.CharField(blank=True,max_length=100)
    Subject = models.CharField(blank=True,max_length=255)
    Message = models.CharField(blank=True,max_length=255)
    Note = models.CharField(blank=True,max_length=255)
    Status = models.CharField(blank=True,choices=STATUS,default='New',max_length=100)
    IP = models.CharField(blank=True,max_length=255)
    Create_at = models.DateTimeField(auto_now_add=True)
    Update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['Name','Email','Subject','Message']
        widgets = {
            'Name' : forms.TextInput(attrs={'class':'input','placeholder':'Name'}),
            'Email': forms.TextInput(attrs={'class':'input','placeholder':'Email'}),
            'Subject': forms.TextInput(attrs={'class':'input','placeholder':'Subject'}),
            'Message': forms.Textarea(attrs={'class':'input','placeholder':'Message'}),
        }

class FAQ(models.Model):
    STATUS =(
    ('T','True'),
    ('F','False'),
    )
    Ordernumber = models.IntegerField()
    Question = models.CharField(max_length=200)
    Answer = RichTextUploadingField()
    Status = models.CharField(max_length=10,choices=STATUS)
    Create_at = models.DateTimeField(auto_now_add=True)
    Update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Question
