from django.db import models
from django.contrib.auth.models import User
from functools import reduce
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.SmallIntegerField(
        choices=(
            (1,'Dollar'), 
            (2, 'So`m')
            )
    ) 
    discount_price = models.DecimalField(
        decimal_places=2, 
        max_digits=10, 
        blank=True, 
        null=True
        )
    baner_image = models.ImageField(upload_to='baner/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


    @property
    def review(self):
        reviews = ProductReview.objects.filter(product_id=self.id)
        result = 0
        for i in reviews:
            result += i.mark
        try:
            result = result / reviews.count()
        except ZeroDivisionError:
            result = 0
        return result
    
    @property 
    def is_discount(self):
        if self.discount_price is None:
            return 0
        return self.discount_price > 0
    
    @property 
    def is_active(self):
        return self.quantity > 0

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mark = models.SmallIntegerField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    @property
    def quantity(self):
        quantity = 0
        products = CartProduct.objects.filter(card_id = self.id)
        for i in products:
            quantity +=i.quantity
        return quantity

    @property
    def total_price(self):
        result = 0
        for i in CartProduct.objects.filter(card_id =self.id):
            result +=(i.product.price)*i.quantity
        return result


class CartProduct(models.Model):
    card = models.ForeignKey(Cart, on_delete=models.CASCADE,)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    @property
    def total_price(self):
        if self.product.is_discount:
            result = self.product.discount_price * self.quantity
        else:
            result = self.product.price * self.quantity
        return result


class ProductIncome(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        self.product_name = self.product.name
        if self.pk:
            enter = ProductIncome.objects.get(pk=self.pk)
            product = enter.product # None/Product
            product.quantity -= enter.amount
            product.quantity += self.amount
            product.save()
            inc = Product_income_outcome.objects.get(type = 1, id = enter.id)
            inc.amount = self.amount
            inc.save()
            super(ProductIncome, self).save(*args, **kwargs)
        else:
            super(ProductIncome, self).save(*args, **kwargs)
            self.product.quantity += self.amount
            self.product.save()
            Product_income_outcome.objects.create(
                product = self.product,
                amount = self.amount,
                foreign_id = self.id,
                type = 1
            )
    def delete(self, *args, **kwargs):
        Product_income_outcome.objects.get(foreign_id = self.pk, type = 1).delete()
        print('hi')
        print('hi2')
        super(ProductIncome, self).delete(*args, **kwargs)
    


class Overall(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    all_outcome = models.IntegerField(default = 0)

    @property
    def all_income(self):
        income = 0
        objs = ProductIncome.objects.filter(product = self.product)
        for obj in objs:
            income += obj.amount
        return income

class ProductOut(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        super(ProductOut, self).save(*args, **kwargs)
        Product_income_outcome.objects.create(
                product = self.product,
                amount = self.amount,
                foreign_id = self.id,
                type = 2
            )
        


class Product_income_outcome(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add = True)
    foreign_id = models.SmallIntegerField()
    type  = models.SmallIntegerField()
    