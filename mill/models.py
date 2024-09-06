from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity_in_stock = models.PositiveIntegerField(default=0, editable=False)
    purchase_price = models.PositiveIntegerField()
    customer_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Production(models.Model):
    production = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='productions')
    quantity = models.PositiveIntegerField()
    production_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Purchase(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='purchases')
    purchase_unit_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    given_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12)
    is_supplier = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Command(models.Model):
    STATE_PAID = 'p'
    STATE_REMAIN = 'r'
    STATE_UNPAID = 'u'
    STATE_CHOICES = [
        (STATE_PAID, 'paid'),
        (STATE_REMAIN, 'remain'),
        (STATE_UNPAID, 'unpaid')
    ]
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='commands')
    state = models.CharField(max_length=1, choices=STATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Item(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='items')
    quantity = models.PositiveIntegerField()
    command = models.ForeignKey(
        Command, on_delete=models.PROTECT, related_name='items')


class ItemReturn(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name='returns')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
