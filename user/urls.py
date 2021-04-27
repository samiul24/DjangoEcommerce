from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('userprofileupdate/', views.userprofileupdate, name='userprofileupdate'),
    path('passwordchange/', views.passwordchange, name='passwordchange'),
    path('order/', views.order, name='order'),
    path('orderdetails/<int:id>', views.orderdetails, name='orderdetails'),
    path('comments/', views.comments, name='comments'),
    path('commentdelete/<int:id>', views.commentdelete, name='commentdelete'),
]
