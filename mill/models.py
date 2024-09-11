from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from mill.constants import STATE_CHOICES, STATE_UNPAID


class Product(models.Model):
    name = models.CharField(max_length=255)
    purchase_price = models.PositiveIntegerField()
    customer_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_quantity_in_stock(self):
        return Product.objects.filter(id=self.id).annotate(
            quantity_in_stock=(
                Coalesce(Sum('purchases__quantity'), Value(0)) +
                Coalesce(Sum('productions__quantity'), Value(0)) -
                Coalesce(Sum('items__quantity'), Value(0)) +
                Coalesce(Sum('items__returns__quantity'), Value(0))
            )
        )\
            .values('quantity_in_stock')\
            .first()['quantity_in_stock']

    def __str__(self) -> str:
        return self.name


class Production(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='productions'
    )
    quantity = models.PositiveIntegerField()
    production_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.production_date}_{self.product.name}'


class Purchase(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT,
        related_name='purchases'
    )
    purchase_unit_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.purchase_date}_{self.product.name}'


class Customer(models.Model):
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12)
    is_supplier = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.given_name} {self.surname}'


class Command(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='commands'
    )
    state = models.CharField(
        max_length=1,
        choices=STATE_CHOICES,
        default=STATE_UNPAID
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_amount(self):
        return sum([item.get_net_quantity() * item.price for item in self.items.all()])

    def __str__(self) -> str:
        return f'{self.pk}'


class Item(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='items'
    )
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    command = models.ForeignKey(
        Command,
        on_delete=models.PROTECT,
        related_name='items'
    )

    def __get_total_returns(self):
        return sum([returned.quantity for returned in self.returns.all()])

    def get_net_quantity(self):
        return self.quantity - self.__get_total_returns()

    def __str__(self) -> str:
        return self.product.name


class ItemReturn(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name='returns')
    quantity = models.PositiveIntegerField()
    return_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Return of {self.quantity} for {self.item}'
