# Generated by Django 5.0.1 on 2024-02-07 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_productincome'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productincome',
            old_name='Product',
            new_name='product',
        ),
    ]
