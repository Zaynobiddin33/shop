from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api import serializers
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Create your views here.

from main import models


@api_view(["GET"])
def index(request):
    q = request.GET.get('q')
    if q:
        products = models.Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    else: 
        products = models.Product.objects.filter(quantity__gt=0)
    categorys = models.Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id:
        products.filter(category_id=category_id)
    
    product_serializer = serializers.ProductSerializer(products, many = True)
    category_serializer = serializers.CategorySerializer(categorys, many = True)
    wishlist_serializer = serializers.WishlistSerializer(models.WishList.objects.all(), many = True)
    context = {
        'products':product_serializer.data,
        'categorys':category_serializer.data,
        'wished': wishlist_serializer.data
    }
    return Response(context)

@api_view(["GET"])
def filtered(request, id):
    products = models.Product.objects.filter(category_id = id)
    context = {

        'categorys': serializers.CategorySerializer(models.Category.objects.all(), many = True).data,
        'products': serializers.ProductSerializer(products, many = True).data
    }
    return Response(context)


@api_view(["GET, POST"])
def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    categorys = models.Category.objects.all()
    recomendation = models.Product.objects.filter(
        category_id=product.category.id).exclude(id=product.id)[:3]
    images = models.ProductImage.objects.filter(product_id=product.id)
    if models.WishList.objects.filter(product = product):
        is_wished = True
    else:
        is_wished = False


    context = {
        'product':serializers.ProductSerializer(product, many = True).data,
        'categorys':serializers.CategorySerializer(categorys, many = True).data,
        'recomendation':serializers.ProductSerializer(recomendation, many = True).data,
        'images':serializers.ProductImageSerializer(images, many = True).data,
        'is_wished': is_wished
    }
    if request.method == 'POST':
        user = request.user
        mark = request.data['rate']
        product = models.Product.objects.get(id = request.data['product_id'])
        if models.ProductReview.objects.filter(user = user, product = product).first():
            data =  models.ProductReview.objects.get(user = user, product = product)
            data.mark = mark
            data.save()
        else:
            models.ProductReview.objects.create(
                product = product,
                user = user,
                mark = mark
            )
    return Response(context)

@api_view(["GET"])
def carts(request):
    active = models.Cart.objects.filter(is_active=True, user=request.user)
    in_active = models.Cart.objects.filter(is_active=False, user=request.user).order_by('-id')
    context = {
        'active':serializers.CartSerializer(active, many = True).data,
        'in_active':serializers.CartSerializer(in_active, many = True).data,
        'categorys': serializers.CategorySerializer(models.Category.objects.all(), many = True).data,
    }
    return Response(context)


@api_view(["GET"])
def cart_detail(request, id):
    cart = models.Cart.objects.get(id=id)
    items = models.CartProduct.objects.filter(card=cart)
    context = {
        'cart':serializers.CartSerializer(cart),
        'items':serializers.CartProductSerializer(items, many = True)
    }
    return Response(context)

@api_view(["GET, POST"])
def login_user(request):
    login_error = False
    if request.method == "POST":
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username,  password=password)
        if user:
            login(request, user)
            return Response({'detail': 'logged in succesully'})
        else:
            return Response({'detail': 'Incorect username or password'})
    return Response({'detail': 'Not in POST'})



@api_view(["GET, POST"])
def regist(request):
    error = False
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        if not models.User.objects.filter(username = username):
            models.User.objects.create_user(
                username=username,
                password=password
            )
            
            user = authenticate(username = username, password = password)
            login(request, user)
            return Response({'detail': 'Registration successful'})
        else:
            return Response({'detail': 'Username exists'})
    return Response({'detail': 'Not in POST'})

@api_view(["GET, POST"])
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return Response({'detail': 'Logout successful'})

    return Response({'detail': 'Not in POST'})

@api_view(["GET, POST"])
@login_required(login_url='main:login')
def create_cart(request, id):           #agar foydalanuvchida Cart bo'lmasa yoki u aktiv bo'lmasa yangi Cart yaratadi
    product = models.Product.objects.get(id = id)
    cart = models.Cart.objects.filter(user = request.user, is_active = True).first()
    if cart:
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data)
    else:
        new_cart = models.Cart.objects.create(
            user = request.user
        )
        serializer = serializers.CartSerializer(new_cart)
        return Response(serializer.data)

@api_view(["GET, POST"])
def add_to_cart(request, id_product, id_user):
    product = models.Product.objects.get(id = id_product)
    cart = models.Cart.objects.get(user_id = id_user, is_active = True)
    previous_url = request.META.get('HTTP_REFERER')
    if models.CartProduct.objects.filter(product_id = id_product, card = cart).first():
        data = models.CartProduct.objects.get(product_id = id_product, card = cart)
        data.quantity +=1
        data.save()
        serializer = serializers.CartProductSerializer(data)
        return Response (serializer.data)
    else:
        data = models.CartProduct.objects.create(
            product = product,
            card = cart,
            )
        serializer = serializers.CartProductSerializer(data)
        return Response (serializer.data)

@api_view(['GET'])
def wishlist(request):
    items = models.WishList.objects.filter(user = request.user)
    context = {
        'items': serializers.WishlistSerializer(items, many = True).data,
        'categorys': serializers.CategorySerializer(models.Category.objects.all(), many = True).data
    }
    return Response(context)

@api_view(['GET'])
def add_wish(request,id):
    if not request.user.is_authenticated:
        return Response({'detail':'not logged in'})
    previous_url = request.META.get('HTTP_REFERER')
    product = models.Product.objects.get(id = id)
    data = models.WishList.objects.create(
        product = product,
        user = request.user
    )
    serializer = serializers.WishlistSerializer(data)
    return Response (serializer.data)

@api_view(['DELETE'])
def delete_wish(request, id):
    try:
        # Check if the wish belongs to the current user
        wish = models.WishList.objects.get(id=id, user=request.user)
    except models.WishList.DoesNotExist:
        return Response({'error': 'Wish not found'})

    wish.delete()
    return Response({'detail': 'Wish deleted successfully'})


@api_view(['POST, GET'])
def user_update(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            new_username = request.data.get('username')
            new_password = request.data.get('password')

            if models.User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                messages.error(request, 'Username is already taken.')
                return Response ({'detail':'username is taken'})
            else:
                user = request.user
                user.username = new_username
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return Response ({'detail':'Updated sucessuflly'})
    
    return Response({'detail': 'Not authenticated user'})

@api_view(['POST, GET'])
def order_cart(request, id):
    cart = models.Cart.objects.get(id=id)
    objects = models.CartProduct.objects.filter(card = cart)
    for obj in objects:
        prod = models.Product.objects.get(id = obj.product.id)
        new_quant = obj.product.quantity-obj.quantity

        if new_quant>=0:
            prod.quantity = new_quant
            prod.save()
            data = models.Overall.objects.get(product = obj.product)
            data.all_outcome +=obj.quantity
            data.save()
            models.ProductOut.objects.create(
                product = prod,
                amount = obj.quantity
            )
        else:
            obj.quantity = prod.quantity
            prod.quantity = 0
            obj.save()
            prod.save()
            data = models.Overall.objects.get(product = obj.product)
            data.all_outcome += obj.quantity
            data.save()
            models.ProductOut.objects.create(
                product = prod,
                amount = obj.quantity
            )

    cart.is_active = False
    cart.save()
    return Response ({'detail':'ordered succesfully'})

@api_view(['GET'])
def cart_detail_delete(request):
    try:
        item_id = request.GET['items_id']
        item = models.CartProduct.objects.get(id=item_id)
        item.delete()
        return Response({'detail': 'Cart item deleted successfully'})
    except models.CartProduct.DoesNotExist:
        return Response({'error': 'Cart item not found'})