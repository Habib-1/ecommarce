from django.contrib import admin
from .models import StockLog
# Register your models here.

class StockLogAdmin(admin.ModelAdmin):
    list_display=('id','product','change_type','quantity','note','created_at',)
    list_display_links=('product',)
    list_filter=('change_type','created_at','product',)
    search_fields=('product__name','note',)


admin.site.register(StockLog,StockLogAdmin)