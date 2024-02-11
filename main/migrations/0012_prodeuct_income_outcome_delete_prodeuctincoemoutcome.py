# Generated by Django 5.0.1 on 2024-02-11 11:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_productout_prodeuctincoemoutcome'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prodeuct_income_outcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('type', models.SmallIntegerField(choices=[(1, 'income'), (1, 'outcome')])),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
        ),
        migrations.DeleteModel(
            name='ProdeuctIncoemoutcome',
        ),
    ]