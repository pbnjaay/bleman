from django.contrib import admin
from .models import Product, Customer

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'purchase_price',
                    'customer_price', 'quantity_in_stock']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['given_name', 'surname', 'is_supplier']
