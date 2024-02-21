from rest_framework.serializers import ModelSerializer
from main.models import (Category, Product, ProductImage, WishList, ProductReview,
                        Cart, CartProduct, ProductIncome, Overall, Product_income_outcome,
                        ProductOut)

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1    

    

class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class WishlistSerializer(ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'


class ProductReviewSerializer(ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


class CartSerializer(ModelSerializer):
    class Meta:
        
        model = Cart
        fields = '__all__'


class CartProductSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = CartProduct
        fields = '__all__'
    

class ProductIncomeSerializer(ModelSerializer):
    class Meta:
        model = ProductIncome
        fields = '__all__'


class OverallSerializer(ModelSerializer):
    class Meta:
        model = Overall
        fields = '__all__'


class ProductOutSerializer(ModelSerializer):
    class Meta:
        model = ProductOut
        fields = '__all__'


class Product_income_outcomeSerializer(ModelSerializer):
    class Meta:
        model = Product_income_outcome
        fields = '__all__'