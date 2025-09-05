from django.contrib import admin
from .models import (
    Category,Brand,Product,Product_Image
)
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name",)}

admin.site.register(Category,CategoryAdmin)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name",)}
    search_fields = ('name', 'sku')

admin.site.register(Product,ProductAdmin)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields={"slug":("name",)}

admin.site.register(Brand,BrandAdmin)

admin.site.register(Product_Image)