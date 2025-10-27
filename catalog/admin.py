from django.contrib import admin
from .models import (
    Category,Brand,Product,Product_Image,Slider,Variant,Size,Color,
      )
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name",)}

admin.site.register(Category,CategoryAdmin)
# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields={"slug":("name",)}
#     search_fields = ('name', 'sku')
#     # list_editable=('is_active','featured')

# admin.site.register(Product,ProductAdmin)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name",)}

admin.site.register(Brand,BrandAdmin)

admin.site.register(Product_Image)

admin.site.register(Slider)

class VariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'price', 'stock']

admin.site.register(Variant,VariantAdmin)
admin.site.register(Size)
admin.site.register(Color)



# Inline configuration for Product Images
class ProductImageInline(admin.TabularInline):
    model = Product_Image
    extra = 1
    fields = ('image', 'is_primary')
    readonly_fields = ()
    show_change_link = True




# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = Product_Image
    extra = 1
    fields = ('image', 'is_primary')
    show_change_link = True


# Inline for Product Variants
class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1
    fields = ('color', 'size', 'price', 'stock')
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'discount_price', 'stock', 'featured', 'is_active')
    list_filter = ('category', 'brand', 'featured', 'is_active')
    search_fields = ('name', 'sku', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    inlines = [ProductImageInline, VariantInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'description', 'category', 'brand')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock', 'sku')
        }),
        ('Status', {
            'fields': ('featured', 'is_active')
        }),
    )

