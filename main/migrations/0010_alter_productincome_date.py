# Generated by Django 5.0.1 on 2024-02-10 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_cartproduct_card_alter_productincome_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productincome',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]