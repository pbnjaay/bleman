from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from mill.constants import STATE_CHOICES, STATE_UNPAID
from mill.models import (Command, Customer, Item, ItemReturn, Product,
                         Production)


class SimpleProductSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'customer_price', 'purchase_price']


class CustomerSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'given_name', 'surname', 'phone_number',
                  'is_supplier', 'created_at', 'updated_at']


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = ['id', 'quantity', 'production_date',
                  'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    quantity_in_stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'customer_price', 'purchase_price',
                  'quantity_in_stock', 'created_at', 'updated_at']


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
                  'price', 'quantity', 'line_amount', 'command']

    line_amount = serializers.SerializerMethodField()

    def get_line_amount(self, item: Item):
        return item.get_net_quantity() * item.price


class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ['id', 'customer', 'state', 'items', 'total_amount']

    items = ItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    state = serializers.ChoiceField(
        choices=STATE_CHOICES,
        default=STATE_UNPAID
    )

    def get_total_amount(self, command: Command):
        return command.get_total_amount()


class UpdateCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Command
        fields = ['state']

    state = serializers.ChoiceField(
        choices=STATE_CHOICES,
        default=STATE_UNPAID
    )


class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['quantity']

    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        item = self.instance
        product = item.product
        quantity_in_stock = product.get_quantity_in_stock()

        if quantity_in_stock < value:
            raise serializers.ValidationError(
                f'{quantity_in_stock} {product.name} left in stock.')

        return value


class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'product_id', 'quantity']

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(required=False)

    def validate_quantity(self, quantity):
        if quantity <= 0:
            raise serializers.ValidationError('must be greater than zero.')

        product_id = int(self.initial_data['product_id'])
        product = Product.objects.filter(pk=product_id).first()
        if product is None:
            raise serializers.ValidationError('not found.')

        quantity_in_stock = product.get_quantity_in_stock()

        if quantity_in_stock < quantity:
            raise serializers.ValidationError(
                f'{quantity_in_stock} {product.name} left in stock.')

        return quantity

    def save(self, **kwargs):
        with transaction.atomic():
            product_id = self.validated_data['product_id']
            command_id = self.context['command_id']
            quantity = self.validated_data['quantity']

            try:
                item = Item.objects.get(
                    command_id=command_id,
                    product=product_id
                )
                item.quantity += quantity
                item.save(update_fields=['quantity'])
                self.instance = item
            except Item.DoesNotExist:
                product = Product.objects.get(pk=product_id)
                command = get_object_or_404(Command, pk=command_id)
                price = product.purchase_price \
                    if command.customer.is_supplier \
                    else product.customer_price
                self.instance = Item.objects.create(
                    command_id=command_id,
                    price=price,
                    **self.validated_data
                )

            return self.instance
