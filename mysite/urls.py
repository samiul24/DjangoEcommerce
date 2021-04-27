from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from home import views
from order import views as orderviews

urlpatterns = [
    path('admin/', admin.site.urls),


    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('user/', include('user.urls')),


    path('about/', views.aboutus, name='aboutus'),
    path('contact/', views.contactus, name='contactus'),
    path('category/<int:id>/<slug:slug>/', views.category_product, name='category_product'),
    path('search/', views.search, name='search_product'),
    path('product/<int:id>/<slug:slug>', views.product_details, name='product_details'),
    path('order/', orderviews.shopcart, name='shopcart' ),
    path('faq/', views.faq, name='faq')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
