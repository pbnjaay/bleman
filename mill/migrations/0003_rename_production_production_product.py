# Generated by Django 5.1.1 on 2024-09-06 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mill', '0002_remove_product_quantity_in_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='production',
            old_name='production',
            new_name='product',
        ),
    ]
