from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from .models import Product, Customer, Production, Purchase, Command, Item

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'purchase_price',
                    'customer_price']
    list_filter = ['created_at']
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['given_name', 'surname', 'is_supplier']
    list_filter = ['is_supplier', 'created_at']
    search_fields = ['given_name__istartswith']


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'production_date']
    list_filter = ['created_at']
    autocomplete_fields = ['product']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['product', 'purchase_unit_price',
                    'quantity', 'purchase_date']
    search_fields = ['product']
    autocomplete_fields = ['product']
    list_filter = ['created_at']


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    autocomplete_fields = ['product']


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'state', 'created_at']
    list_filter = ['state', 'created_at']
    inlines = [ItemInline]
    autocomplete_fields = ['customer']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'quantity', 'command']

    def save_model(self, request, obj, form, change):
        obj.update_quantity(form.cleaned_data['quantity'])
        return super().save_model(request, obj, form, change)
