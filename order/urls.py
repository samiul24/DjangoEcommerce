from django.urls import path, include
from . import views
#from product import views

app_name='Order'

urlpatterns = [
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deleteformshopcart/<int:id>', views.deleteformshopcart, name='deleteformshopcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
]
