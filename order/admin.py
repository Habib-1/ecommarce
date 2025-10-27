from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress

# Inline configuration for displaying Order Items within Order admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'size', 'color', 'quantity', 'price')
    show_change_link = True


# Custom admin action to mark orders as delivered
@admin.action(description="✅ Mark selected orders as Delivered")
def mark_delivered(modeladmin, request, queryset):
    queryset.update(order_status='delivered')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'order_status', 'payment_status',
        'total_amount', 'shipping_charge', 'created_at'
    )
    list_filter = (
        'order_status', 'payment_status', 'created_at',
        'shipping_address__country', 'shipping_address__city'
    )
    search_fields = (
        'customer__name', 'customer__email',
        'shipping_address__full_name', 'shipping_address__phone',
        'shipping_address__postal_code'
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    actions = [mark_delivered]

    fieldsets = (
        ('Order Summary', {
            'fields': ('customer', 'order_status', 'payment_status', 'total_amount', 'shipping_charge')
        }),
        ('Shipping Information', {
            'fields': (
                'shipping_full_name', 'shipping_phone', 'shipping_street',
                'shipping_city', 'shipping_state', 'shipping_postal_code',
                'shipping_country', 'shipping_note'
            ),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = (
        'shipping_full_name', 'shipping_phone', 'shipping_street',
        'shipping_city', 'shipping_state', 'shipping_postal_code',
        'shipping_country', 'shipping_note'
    )

    # Shipping info display methods
    def shipping_full_name(self, obj):
        return getattr(obj.shipping_address, 'full_name', '-') if obj.shipping_address else "-"
    shipping_full_name.short_description = "Full Name"

    def shipping_phone(self, obj):
        return getattr(obj.shipping_address, 'phone', '-') if obj.shipping_address else "-"
    shipping_phone.short_description = "Phone"

    def shipping_street(self, obj):
        return getattr(obj.shipping_address, 'street', '-') if obj.shipping_address else "-"
    shipping_street.short_description = "Street"

    def shipping_city(self, obj):
        return getattr(obj.shipping_address, 'city', '-') if obj.shipping_address else "-"
    shipping_city.short_description = "City"

    def shipping_state(self, obj):
        return getattr(obj.shipping_address, 'state', '-') if obj.shipping_address else "-"
    shipping_state.short_description = "State"

    def shipping_postal_code(self, obj):
        return getattr(obj.shipping_address, 'postal_code', '-') if obj.shipping_address else "-"
    shipping_postal_code.short_description = "Postal Code"

    def shipping_country(self, obj):
        return getattr(obj.shipping_address, 'country', '-') if obj.shipping_address else "-"
    shipping_country.short_description = "Country"

    def shipping_note(self, obj):
        return getattr(obj.shipping_address, 'note', '-') if obj.shipping_address else "-"
    shipping_note.short_description = "Note"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'size', 'color', 'quantity', 'price')
    list_filter = ('product', 'size', 'color',)
    search_fields = ('product__name', 'size', 'color',)
    ordering = ('-order__created_at',)


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'city', 'state', 'postal_code', 'country')
    search_fields = ('full_name', 'phone', 'postal_code', 'country')
    list_filter = ('country', 'state', 'city')
    ordering = ('-id',)
