from django.contrib import admin
from orders.models import Order, OrderItem


class RelationshipInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'status',
                    'total_item', 'sum_order', 'created_at')
    inlines = [RelationshipInline]
