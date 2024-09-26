# Generated by Django 5.1.1 on 2024-09-26 09:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mill', '0010_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('CASH', 'Cash'), ('CREDIT_CARD', 'Credit Card'), ('BANK_TRANSFER', 'Bank Transfer')], default='CASH', max_length=15),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.PositiveBigIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='command',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='mill.command'),
        ),
    ]
