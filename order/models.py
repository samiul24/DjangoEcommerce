from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from django import forms

# Create your models here.
class ShopCart(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Quantity = models.IntegerField()

    def __str__(self):
        return self.Product.Title


    @property
    def price(self):
        return (self.Product.Price)

    @property
    def amount(self):
        return (self.Quantity*self.Product.Price)

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Code = models.CharField(max_length=5, editable=False )
    First_name = models.CharField(max_length=10)
    Last_name = models.CharField(max_length=10)
    Phone = models.CharField(blank=True, max_length=20)
    Address = models.CharField(blank=True, max_length=150)
    City = models.CharField(blank=True, max_length=20)
    Country = models.CharField(blank=True, max_length=20)
    Total = models.FloatField()
    Status=models.CharField(max_length=10,choices=STATUS,default='New')
    Ip = models.CharField(blank=True, max_length=20)
    Adminnote = models.CharField(blank=True, max_length=100)
    Create_at=models.DateTimeField(auto_now_add=True)
    Update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.User.first_name

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['First_name','Last_name','Address','Phone','City','Country']

class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    Quantity = models.IntegerField()
    Price = models.FloatField()
    Amount = models.FloatField()
    Status = models.CharField(max_length=10, choices=STATUS, default='New')
    Create_at = models.DateTimeField(auto_now_add=True)
    Update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Product.Title
