# Generated by Django 4.0.4 on 2022-04-30 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0003_offer_external_ms_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='product_app.product'),
        ),
    ]
