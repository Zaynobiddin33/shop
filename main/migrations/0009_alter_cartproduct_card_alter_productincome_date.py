# Generated by Django 5.0.1 on 2024-02-10 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_overall_all_outcome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cart', unique=True),
        ),
        migrations.AlterField(
            model_name='productincome',
            name='date',
            field=models.DateTimeField(blank=True),
        ),
    ]
