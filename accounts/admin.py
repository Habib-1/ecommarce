from django.contrib import admin
from .models import User,Customer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display=('id','email','name','phone', 'is_active', 'is_staff')
    list_display_links=('email',)
    ordering=['email']
    search_fields = ('email', 'name', 'phone')
    readonly_fields = ('date_joined', 'last_login','created_at','updated_at',)

    fieldsets=(
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':('name','phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff','is_admin', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined','created_at','updated_at',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser','is_admin',),
        }),
    )

  
admin.site.register(User,UserAdmin)
admin.site.register(Customer)