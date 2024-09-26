# Generated by Django 5.1.1 on 2024-09-26 07:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mill', '0009_alter_command_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveBigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('command', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='mill.command')),
            ],
        ),
    ]