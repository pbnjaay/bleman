# Generated by Django 5.1.1 on 2024-09-26 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mill', '0012_order_alter_item_command_alter_payment_command_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='command',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='command',
            new_name='order',
        ),
    ]
