from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from product.models import Product,Category,Comments,CommentForm
import json

# Create your views here.
def index(request):
    return  HttpResponse('This is product page')

def search_auto(request):
    #print(request.GET)
    userSearching = request.GET.get('term')
    #print(userSearching)
    data = Product.objects.filter(Title__icontains=userSearching)
    productlist = []
    productlist += [x.Title for x in data]
    #print(productlist)
    return JsonResponse(productlist,safe=False)


def comment(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    form = CommentForm()
    if request.method=='POST':
        data = Comments() # Create a relation with Comment Model
        form = CommentForm(request.POST)
        if form.is_valid():
            #print(id)
            data.Product_id = id
            data.Subject = form.cleaned_data['Subject']
            data.Comment = form.cleaned_data['Comment']
            data.Rating = form.cleaned_data['Rating']
            current_user = request.user
            #print(current_user)
            data.User_id = current_user.id
            #print(data.User_id)
            data.save()
            messages.success(request,'Thanks for your review')
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)
