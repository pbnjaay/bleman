from django.contrib import admin
from .models import Product, Customer, Production, Purchase, Command, Item

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'purchase_price',
                    'customer_price']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['given_name', 'surname', 'is_supplier']


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'production_date']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['product', 'purchase_unit_price',
                    'quantity', 'purchase_date']


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ['customer', 'state']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'quantity', 'command']
