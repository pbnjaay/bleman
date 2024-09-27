# Generated by Django 5.1.1 on 2024-09-26 21:35

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mill', '0013_rename_command_item_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('CASH', 'cash'), ('CREDIT_CARD', 'credit Card'), ('BANK_TRANSFER', 'bank Transfer')], default='CASH', max_length=15),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('COMPLETED', 'completed'), ('FAILED', 'failed')], default='PENDING', max_length=10),
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('return_date', models.DateTimeField(auto_now_add=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='returns', to='mill.item')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.DeleteModel(
            name='ItemReturn',
        ),
    ]