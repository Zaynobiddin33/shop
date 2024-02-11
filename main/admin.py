from django.contrib import admin
from . import models


admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.Cart)
admin.site.register(models.CartProduct)
admin.site.register(models.WishList)
admin.site.register(models.ProductReview)
admin.site.register(models.ProductIncome)
admin.site.register(models.Overall)
admin.site.register(models.ProductOut)
admin.site.register(models.Product_income_outcome)