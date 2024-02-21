# Generated by Django 5.0.1 on 2024-02-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_alter_cartproduct_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='overall',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='product_income_outcome',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='productimage',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='productincome',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='productout',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='productreview',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
