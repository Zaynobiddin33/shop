from rest_framework.serializers import ModelSerializer
from main import models

class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = '__all__'


class WishlistSerializer(ModelSerializer):
    class Meta:
        model = models.WishList
        fields = '__all__'


class ProductReviewSerializer(ModelSerializer):
    class Meta:
        model = models.ProductReview
        fields = '__all__'


class CartSerializer(ModelSerializer):
    class Meta:
        model = models.Cart
        fields = '__all__'


class CartProductSerializer(ModelSerializer):
    class Meta:
        model = models.CartProduct
        fields = '__all__'
    

class ProductIncomeSerializer(ModelSerializer):
    class Meta:
        model = models.ProductIncome
        fields = '__all__'


class OverallSerializer(ModelSerializer):
    class Meta:
        model = models.Overall
        fields = '__all__'


class ProductOutSerializer(ModelSerializer):
    class Meta:
        model = models.ProductOut
        fields = '__all__'


class Product_income_outcomeSerializer(ModelSerializer):
    class Meta:
        model = models.Product_income_outcome
        fields = '__all__'