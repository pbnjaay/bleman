from django.db.models import Manager
from django.db import transaction
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

from mill import models


class ProductManager(Manager):
    def get_product_with_quantity_in_stock(self):
        return models.Product.objects.annotate(
            quantity_in_stock=(
                Coalesce(Sum('purchases__quantity'), Value(0)) +
                Coalesce(Sum('productions__quantity'), Value(0)) -
                Coalesce(Sum('items__quantity'), Value(0)) +
                Coalesce(Sum('items__returns__quantity'), Value(0))
            )
        )


class ItemManager(Manager):
    def add_item(self, command, product, quantity, price):
        with transaction.atomic():
            item, created = models.Item.objects.get_or_create(
                command=command,
                product=product,
                defaults={'quantity': quantity, 'price': price}
            )

            if not created:
                item.update_quantity(item.quantity + quantity)

            return item
