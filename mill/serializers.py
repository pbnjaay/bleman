from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from mill.constants import ORDER_STATUS_CHOICES, ORDER_STATUS_UNPAID
from mill.models import (Order, Customer, Item, ItemReturn, Payment, Product, Purchase,
                         Production)


class ProductSerializer(serializers.ModelSerializer):
    quantity_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'customer_price', 'purchase_price',
                  'quantity_in_stock', 'created_at', 'updated_at']


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ['id', 'product', 'quantity', 'production_date',
                  'created_at', 'updated_at']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'product', 'purchase_unit_price',
                  'quantity', 'purchase_date', 'created_at', 'updated_at']


class CustomerSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'given_name', 'surname', 'phone_number',
                  'is_supplier', 'created_at', 'updated_at']


class ItemReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemReturn
        fields = ['id', 'quantity', 'return_date',
                  'reason', 'created_at', 'updated_at']

    def create(self, validated_data):
        item_id = self.context['item_id']
        return ItemReturn.objects.create(item_id=item_id, **validated_data)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'product',
                  'price', 'quantity', 'line_amount', 'order']

    line_amount = serializers.SerializerMethodField()

    def get_line_amount(self, item: Item):
        return item.get_net_quantity() * item.price


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'items', 'total_amount']

    items = ItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    status = serializers.ChoiceField(
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_UNPAID,
    )

    def get_total_amount(self, order: Order):
        return order.get_total_amount()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'order', 'status', 'method']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['state']

    state = serializers.ChoiceField(
        choices=ORDER_STATUS_CHOICES,
        default=ORDER_STATUS_UNPAID
    )


class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['quantity']

    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        item = self.instance
        product = item.product
        product.validate_stock_availability(value)
        return value


class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity']

    quantity = serializers.IntegerField(required=False)

    def save(self, **kwargs):
        order_id = self.context['order_id']
        product = self.validated_data['product']
        order = get_object_or_404(Order, pk=order_id)
        quantity = self.validated_data['quantity']
        price = product.purchase_price \
            if order.customer.is_supplier\
            else product.customer_price
        try:
            item = Item.objects.add_item(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )
        except ValidationError as e:
            raise serializers.ValidationError(
                {"quantity": list(e)}, code='invalid'
            )
        return item
