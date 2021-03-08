from django.contrib import admin
from catalog.models import Collection, Product


@admin.register(Collection)
class ProductCollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
