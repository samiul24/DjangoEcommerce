from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from order.models import ShopCart
from order.forms import ShopCartForm
from order.models import Order, OrderForm, OrderProduct
from product.models import Category, Product
from home.models import Setting
from user.models import UserProfile

from django.db.models import Avg, Max, Min, Sum
from django.utils.crypto import get_random_string


@login_required(login_url='/user/login/') # Check login
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkproduct = ShopCart.objects.filter(Product_id=id, User_id=current_user.id)

    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method=='POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1:
                data = ShopCart.objects.get(Product_id=id, User_id=current_user.id)
                data.Quantity += form.cleaned_data['Quantity']
                data.save()
            else:
                data = ShopCart()
                data.User_id = current_user.id
                data.Product_id = id
                data.Quantity = form.cleaned_data['Quantity']
                data.save()
        messages.success(request,'Product Added to Shop Cart')

    else:
        if control==1:
            data = ShopCart.objects.get(Product_id=id, User_id=current_user.id)
            data.Quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.User_id = current_user.id
            data.Product_id = id
            data.Quantity = 1
            data.save()
        messages.success(request,'Product Added to Shop Cart')

    return HttpResponseRedirect(url)

def shopcart(request):
    category = Category.objects.all()
    setting = Setting.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(User_id=current_user.id)
    orderqty = ShopCart.objects.filter(User_id=current_user.id).aggregate(Sum('Quantity'))
    orderqty = orderqty['Quantity__sum']

    total = 0
    for sctotal in shopcart:
        total += sctotal.Quantity * sctotal.Product.Price

    context ={
        'category':category,
        'setting':setting,
        'shopcart':shopcart,
        'orderqty':orderqty,
        'total':total,
    }
    return render(request,'ShopCart_Products.html', context)

@login_required(login_url='/user/login/') # Check login
def deleteformshopcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request,'Remove From Shop Cart')
    return HttpResponseRedirect('/order/')


def orderproduct(request):
    #form = OrderForm()
    category = Category.objects.all()
    setting = Setting.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(User_id=current_user.id)
    shopcart = ShopCart.objects.filter(User_id=current_user.id)
    orderqty = ShopCart.objects.filter(User_id=current_user.id).aggregate(Sum('Quantity'))
    orderqty = orderqty['Quantity__sum']
    #print(orderqty)

    total = 0
    for sctotal in shopcart:
        total += sctotal.Quantity * sctotal.Product.Price
        #print(total)

    if request.method=='POST':
        form = OrderForm(request.POST)
        #print(form)
        #print(request.POST['First_name'])
        if form.is_valid():
            data = Order()
            data.First_name=form.cleaned_data['First_name']
            data.Last_name=form.cleaned_data['Last_name']
            data.City=form.cleaned_data['City']
            data.Country=form.cleaned_data['Country']
            data.Phone=form.cleaned_data['Phone']
            data.Address=form.cleaned_data['Address']
            data.User_id=current_user.id
            data.Total=total
            data.Ip=request.META.get('REMOTE_ADDR')
            ordercode=get_random_string(5).upper()
            data.Code=ordercode
            #print(ordercode)
            data.save()

            shopcart = ShopCart.objects.filter(User_id=current_user.id)
            for sc in shopcart:
                orderdetails=OrderProduct()
                orderdetails.Order_id = data.id
                orderdetails.User_id = current_user.id
                orderdetails.Product_id = sc.Product_id
                #print(orderdetails.Product_id)
                orderdetails.Quantity = sc.Quantity
                orderdetails.Price = sc.Product.Price
                #orderdetails.Price = sc.price
                orderdetails.Amount = sc.amount
                #orderdetails.Amount = sc.Product.Price * sc.Quantity
                orderdetails.save()

                #Quantity Deduction From Stock
                product = Product.objects.get(id=sc.Product_id)
                product.Amount -= sc.Quantity
                product.save()

            shopcart = ShopCart.objects.filter(User_id=current_user.id).delete()
            request.session['cart_items']=0
            messages.success(request,'Your order is completed successfully')
            context={
                'ordercode':ordercode,
                'category':category,
                'setting':setting,
            }
            return render(request,'order_complete.html',context)

        else:
            #Need to code another system here. This only for test basis
            print('Form is not valid')
    else:
        #Need to code another system here. This only for test basis
        print('Form is not posted')

    context ={
        'category':category,
        'setting':setting,
        'shopcart':shopcart,
        'orderqty':orderqty,
        'total':total,
        'profile':profile,
    }
    return render(request,'order_form.html', context)
