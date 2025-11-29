from django.contrib import admin
from .models import Order, OrderItem, Escrow


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['tier_multiplier', 'final_price', 'created_at']
    fields = ['project', 'tier', 'base_price', 'tier_multiplier', 'final_price', 'freelancer']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'client', 'status', 'total_amount', 'created_at', 'paid_at']
    list_filter = ['status', 'created_at', 'paid_at']
    search_fields = ['order_number', 'client__username', 'client__email']
    readonly_fields = ['order_number', 'total_amount', 'created_at', 'updated_at', 'paid_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'client', 'status', 'total_amount')
        }),
        ('Payment Details', {
            'fields': ('payment', 'paid_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'project', 'tier', 'base_price', 'tier_multiplier', 'final_price', 'freelancer']
    list_filter = ['tier', 'created_at']
    search_fields = ['order__order_number', 'project__title', 'freelancer__username']
    readonly_fields = ['tier_multiplier', 'final_price', 'created_at']


@admin.register(Escrow)
class EscrowAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'status', 'held_at', 'released_at', 'refunded_at']
    list_filter = ['status', 'held_at', 'released_at']
    search_fields = ['order__order_number', 'order__client__username']
    readonly_fields = ['held_at', 'released_at', 'refunded_at']
    
    fieldsets = (
        ('Escrow Information', {
            'fields': ('order', 'amount', 'status')
        }),
        ('Timestamps', {
            'fields': ('held_at', 'released_at', 'refunded_at')
        }),
    )
