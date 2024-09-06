from rest_framework import serializers

from mill.models import Customer, Product


class ProductSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'customer_price', 'purchase_price']


class CustomerSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'given_name', 'surname', 'phone_number', 'is_supplier']
