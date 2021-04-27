from django.contrib import admin
from product.models import Category, Product, Images, Comments, Color, Size, Variants
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Title','parent','Status']
    list_filter = ['Status',]

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "Title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'Slug': ('Title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'Category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'Category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ['id','image_tag']
    extra = 5

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['Title','Category','Status', 'image_tag']
    list_filter = ['Category','Status', ]
    readonly_fields =('image_tag',)
    inlines = [ProductImageInline,ProductVariantsInline]
    prepopulated_fields = {'Slug': ('Title',)}

class CommentsAdmin(admin.ModelAdmin):
    list_display = ['Subject','Comment','Status','Rating','Create_at']
    list_filter = ['Status','Rating', ]
    readonly_fields =('Rating','Comment',)

class ColorAdmin(admin.ModelAdmin):
    list_display=['Name','Code','color_tag']

class SizeAdmin(admin.ModelAdmin):
    list_display=['Name','Code']

class VariantsAdmin(admin.ModelAdmin):
    list_display = ['title','product','color','size','price','quantity','image_tag']

admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Variants,VariantsAdmin)
