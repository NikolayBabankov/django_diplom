from django.contrib import admin
from api_shop.models import Product, Review, Order, OrderItem,Collection


class RelationshipInline(admin.TabularInline):
    model = OrderItem
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','creator', 'status','total_item','sum_order','created_at')
    inlines = [RelationshipInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price' )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Collection)
class ProductCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description' )



