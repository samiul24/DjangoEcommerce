from django.db import models
from django import forms
from django.utils.safestring import SafeData, SafeString, mark_safe
from django.db.models import Count, Avg
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.contrib.auth.models import User



# Create your models here.
class Category(MPTTModel):
    STATUS = (
        ('True','True'),
        ('False','False'),
    )
    parent      = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    Title       = models.CharField(max_length=20)
    Keywords    = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Image       = models.ImageField(blank=True, upload_to='images/')
    Status      = models.CharField(max_length=10, choices=STATUS)
    Slug        = models.SlugField(null=False, unique=True)
    Create_at   = models.DateTimeField(auto_now_add=True)
    Update_at   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Title

    class MPTTMeta:
        order_insertion_by = ['Title']


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    VARIANTS=(
        ('None','None'),
        ('Size','Size'),
        ('Color','Color'),
        ('Size-Color','Size-Color'),
    )
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Title    = models.CharField(max_length=255)
    Keywords = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Variant = models.CharField(max_length=15, choices=VARIANTS, default='None')
    Image = models.ImageField(blank=False, upload_to='images/')
    Price = models.FloatField()
    Amount = models.IntegerField()
    MinAmount = models.IntegerField()
    Details = RichTextUploadingField()
    Slug = models.CharField(max_length=255, null=False, unique=True)
    Status = models.CharField(max_length=10, choices=STATUS)
    Create_at = models.DateTimeField(auto_now_add=True)
    Update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Title

    #def image_tag(self):
        #return mark_safe('<img src="{}" width="80" height="50"/>'.format(self.Image.url))  # Get Image url

    def image_tag(self):
        if self.Image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.Image.url))
        else:
            return ""

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


    def avaregereview(self):
        reviews = Comments.objects.filter(Product=self).aggregate(avarage=Avg('Rating'))
        avg=0
        #print(avg)
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
            #print(avg)
        return avg

    def countreview(self):
        reviews = Comments.objects.filter(Product=self).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

class Images(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Title = models.CharField(max_length=255)
    Image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.Title

    def image_tag(self):
        if self.Image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.Image.url))
        else:
            return ""


class Comments(models.Model):
    STATUS =(
    ('New','New'),
    ('True','True'),
    ('False','False'),
    )
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Subject = models.CharField(max_length=50)
    Comment = models.CharField(max_length=250)
    Rating = models.IntegerField()
    Status = models.CharField(max_length=5,choices=STATUS,default='New')
    Create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Subject

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['Subject','Comment','Rating',]


class Color(models.Model):
    Name = models.CharField(max_length=25)
    Code = models.CharField(max_length=50)

    def __str__(self):
        return self.Name

    def color_tag(self):
        if self.Code is not None:
            return mark_safe('<p style="background-color:{}">Color</p>'.format(self.Code))
        else:
            return ""
    color_tag.short_description = 'Color'
    color_tag.allow_tags = True


class Size(models.Model):
    Name = models.CharField(max_length=25)
    Code = models.CharField(max_length=50)

    def __str__(self):
        return self.Name

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.Image.url))
        else:
            return ""
