from django.contrib import admin
from .models import Product, Customer, Production, Purchase, Command, Item

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'purchase_price',
                    'customer_price']
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['given_name', 'surname', 'is_supplier']
    list_filter = ['is_supplier']
    search_fields = ['given_name__istartswith']


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'production_date']
    autocomplete_fields = ['product']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['product', 'purchase_unit_price',
                    'quantity', 'purchase_date']
    search_fields = ['product']
    autocomplete_fields = ['product']


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    autocomplete_fields = ['product']


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'state']
    list_filter = ['state']
    inlines = [ItemInline]
    autocomplete_fields = ['customer']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'quantity', 'command']
