from django.contrib import admin
from order.models import ShopCart, Order, OrderProduct

# Register your models here.

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['User','Product','Quantity','price','amount',]
    list_filter = ['User','Product','Quantity']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('User', 'Product','Price','Quantity','Amount')
    can_delete = False
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['First_name', 'Last_name','Phone','City','Total','Status']
    list_filter = ['Status']
    readonly_fields = ('User','Address','City','Country','Phone','First_name','Ip', 'Last_name','Phone','City','Total')
    can_delete = False
    inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['User', 'Product','Price','Quantity','Amount']
    list_filter = ['Status']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
