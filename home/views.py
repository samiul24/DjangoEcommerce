from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from . import models
from home.models import ContactMessage, ContactForm
from product.models import Category, Product, Images, Comments
from order.models import ShopCart
from home.forms import SearchForm
from django.db.models import Avg, Max, Min, Sum, Count
import json


# Create your views here.
def index(request):
    setting = models.Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]
    products_latest = Product.objects.all().order_by('-id')[:4]
    products_picked = Product.objects.all().order_by('?')[:4]
    page = 'home'
    current_user = request.user
    orderqty = ShopCart.objects.filter(User_id=current_user.id).aggregate(Sum('Quantity'))
    orderqty = orderqty["Quantity__sum"]
    shopcart = ShopCart.objects.filter(User_id=current_user.id)

    total = 0
    for sctotal in shopcart:
        total += sctotal.Quantity * sctotal.Product.Price

    context = {
        'setting':setting,
        'page':page,
        'category':category,
        'products_slider':products_slider,
        'products_latest':products_latest,
        'products_picked':products_picked,
        'orderqty':orderqty,
        'shopcart':shopcart,
        'total':total,
    }
    return render(request, 'index.html', context)

def aboutus(request):
    category = Category.objects.all()
    setting = models.Setting.objects.get(pk=1)
    context={
        'setting':setting,
        'category':category,
        }
    return render(request, 'about.html', context )

def contactus(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        #print(form)
        if form.is_valid():
            data = ContactMessage() #Its a model and Just for data checking with model field. If it does not check then also data will save
            data.Name = form.cleaned_data['Name']
            data.Email = form.cleaned_data['Email']
            data.Subject = form.cleaned_data['Subject']
            data.Message = form.cleaned_data['Message']
            data.ip = request.META.get('REMOTE_ADDR')
            #print(data.ip)
            #print(data.Message)
            data.save()
            messages.success(request,'Thanks for your message')
            #form.save() # Direct ata dileo hobe
            return HttpResponseRedirect('/contact')

    setting = models.Setting.objects.get(pk=1)
    form = models.ContactForm()

    current_user = request.user
    orderqty = ShopCart.objects.filter(User_id=current_user.id).aggregate(Sum('Quantity'))
    orderqty = orderqty["Quantity__sum"]
    shopcart = ShopCart.objects.filter(User_id=current_user.id)

    total = 0
    for sctotal in shopcart:
        total += sctotal.Quantity * sctotal.Product.Price

    context={
        'setting':setting,
        'form':form,
        'category':category,
        'orderqty':orderqty,
        'shopcart':shopcart,
        'total':total,
        }
    return render(request, 'contact.html', context)

def category_product(request,id,slug):
    setting = models.Setting.objects.get(pk=1)
    category = Category.objects.all()
    products = Product.objects.filter(Category_id=id)
    context = {
        'setting':setting,
        'category':category,
        'product':products,
        }
    return render(request, 'category_product.html', context)


def search(request):
    setting = models.Setting.objects.get(pk=1)
    if request.method=="POST":
        category = Category.objects.all()
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            print(query)
            catid = form.cleaned_data['catid']
            if catid==0:
                products = Product.objects.filter(Title__icontains=query)
            else:
                products = Product.objects.filter(Title__icontains=query,Category_id=catid)

        current_user = request.user
        orderqty = ShopCart.objects.filter(User_id=current_user.id).aggregate(Sum('Quantity'))
        orderqty = orderqty["Quantity__sum"]
        shopcart = ShopCart.objects.filter(User_id=current_user.id)

        total = 0
        for sctotal in shopcart:
            total += sctotal.Quantity * sctotal.Product.Price
            context ={
                'setting':setting,
                'category':category,
                'products':products,
                'query':query,
                'orderqty':orderqty,
                'shopcart':shopcart,
                'total':total,
            }
            return render(request, 'search_product.html', context)
    return HttpResponseRedirect('/')

def product_details(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(Product_id=id)
    comments = Comments.objects.filter(Product_id=id)
    commentscount = Comments.objects.filter(Product_id=id).count()
    current_user = request.user
    orderqty = ShopCart.objects.filter(User_id=current_user.id).aggregate(Sum('Quantity'))
    orderqty = orderqty["Quantity__sum"]
    shopcart = ShopCart.objects.filter(User_id=current_user.id)

    total = 0
    for sctotal in shopcart:
        total += sctotal.Quantity * sctotal.Product.Price

    context = {
        'category':category,
        'product':product,
        'images':images,
        'comments':comments,
        'cc':commentscount,
        'orderqty':orderqty,
        'shopcart':shopcart,
        'total':total,
    }
    return render(request, 'product_details.html', context)

def faq(request):
    setting = models.Setting.objects.get(pk=1)
    category = Category.objects.all()
    faq = models.FAQ.objects.filter(Status="T").order_by("Ordernumber")
    context={
        'setting':setting,
        'category':category,
        'faq': faq,
    }
    return render(request, 'faq.html', context)
