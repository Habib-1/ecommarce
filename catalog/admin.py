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

admin.site.register(Product,ProductAdmin)
admin.site.register(Brand)

admin.site.register(Product_Image)