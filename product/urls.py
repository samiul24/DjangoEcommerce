from django.urls import path, include
from . import views
#from product import views

app_name='Product'

urlpatterns = [
    path('', views.index, name='index'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('comment/<int:id>/', views.comment, name='comment'),
]
