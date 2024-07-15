# Generated by Django 5.0.4 on 2024-07-10 01:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.group'),
        ),
    ]