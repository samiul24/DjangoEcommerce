from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from user.forms import UserLoginForm, SignUpForm, UserUpdateForm, ProfileUpdateForm

from home.models import Setting
from product.models import Category, Comments
from user.models import UserProfile
from order.models import Order, OrderProduct



# Create your views here.
def index(request):
    return HttpResponse('User App')

def login_view(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = UserLoginForm()
    context={}
    loginerror=False
    if request.method=='POST':
        #This is a manul process, we can do it as per framing short way
        data = User()
        form = UserLoginForm(request.POST)

        if form.is_valid():
            data.username=form.cleaned_data['username']
            username=data.username
            data.password=form.cleaned_data['password']
            password=data.password

            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                current_user=request.user
                userprofile=UserProfile.objects.get(user_id=current_user.id)
                request.session['userimage']=userprofile.Image.url
                return HttpResponseRedirect('/')
            else:
                loginerror=True
                context={
                    'loginerror':loginerror,
                    'setting':setting,
                    'category':category,
                }
                return render(request,'login.html',context)

    context ={
        'setting':setting,
        'category':category,
    }
    return render(request,'login.html',context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = SignUpForm()
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password)
            login(request,user)
            data = UserProfile()
            current_user = request.user
            data.User_id = current_user.id
            data.Image = 'images/user/user.png'
            data.save()
            messages.success(request,'Your account is created')
            return HttpResponseRedirect('/')
    context={
        'setting':setting,
        'category':category,
        'form':form,
    }
    return render(request,'signup.html',context)

def userprofile(request):
        category = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        current_user=request.user
        profile = UserProfile.objects.get(pk=current_user.id)
        context={
            'setting':setting,
            'category':category,
            'profile':profile,
            }
        return render(request,'userprofile.html',context)

def userprofileupdate(request):
            category = Category.objects.all()
            setting = Setting.objects.get(pk=1)

            if request.method=='POST':
                user_form = UserUpdateForm(request.POST, instance=request.user)
                profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    profile_form.save()
                    messages.success(request,'Successfully Profile Updated')
                    return HttpResponseRedirect('/user/userprofile/')
            else:
                user_form = UserUpdateForm(instance=request.user)
                profile_form = ProfileUpdateForm(instance=request.user.userprofile)
                context={
                    'setting':setting,
                    'category':category,
                    'user_form':user_form,
                    'profile_form':profile_form,
                    }
            return render(request,'userprofileupdate.html',context)


@login_required(login_url='/login') # Check login
def passwordchange(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user/userprofile')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/passwordchange')
    else:
        form = PasswordChangeForm(request.user)
        context={
            'category':category,
            'setting':setting,
            'form':form,
            }
        return render(request, 'userpasswordchange.html', context)

@login_required(login_url='/login')
def order(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user=request.user
    orders = Order.objects.filter(User_id=current_user.id)
    context={
        'category':category,
        'setting':setting,
        'orders':orders,
        }
    return render(request, 'order.html', context)


@login_required(login_url='/login')
def orderdetails(request,id):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user=request.user
    order = Order.objects.get(id=id)
    orderproduct = OrderProduct.objects.filter(Order_id=id)
    context={
        'category':category,
        'setting':setting,
        'order':order,
        'orderproduct':orderproduct,
        }
    return render(request, 'orderdetails.html', context)


@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    current_user=request.user
    comments = Comments.objects.filter(User_id=current_user.id)
    context={
        'category':category,
        'setting':setting,
        'comments':comments,
        }
    return render(request, 'comments.html', context)


@login_required(login_url='/login')
def commentdelete(request,id):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    Comments.objects.filter(id=id).delete()
    messages.success(request, 'Comment Deleted')
    return HttpResponseRedirect('/user/comments')
