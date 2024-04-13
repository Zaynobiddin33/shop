from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from api import serializers
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import update_session_auth_hash
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.authentication import *
from rest_framework.permissions import IsAuthenticated
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
def filtered(request, slug):
    products = models.Product.objects.filter(category__slug = slug)
    context = {

        'categorys': serializers.CategorySerializer(models.Category.objects.all(), many = True).data,
        'products': serializers.ProductSerializer(products, many = True).data
    }
    return Response(context)


# @api_view(["GET, POST"])
# def product_detail(request, id):
#     product = models.Product.objects.get(id=id)
#     categorys = models.Category.objects.all()
#     recomendation = models.Product.objects.filter(
#         category_id=product.category.id).exclude(id=product.id)[:3]
#     images = models.ProductImage.objects.filter(product_id=product.id)
#     if models.WishList.objects.filter(product = product):
#         is_wished = True
#     else:
#         is_wished = False



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
def cart_detail(request, slug ):
    cart = models.Cart.objects.get(slug =slug )
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
def create_cart(request, slug):           #agar foydalanuvchida Cart bo'lmasa yoki u aktiv bo'lmasa yangi Cart yaratadi
    product = models.Product.objects.get(slug = slug)
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
def add_wish(request,slug):
    if not request.user.is_authenticated:
        return Response({'detail':'not logged in'})
    previous_url = request.META.get('HTTP_REFERER')
    product = models.Product.objects.get(slug = slug)
    data = models.WishList.objects.create(
        product = product,
        user = request.user
    )
    serializer = serializers.WishlistSerializer(data)
    return Response (serializer.data)

@api_view(['DELETE'])
def delete_wish(request, slug ):
    try:
        # Check if the wish belongs to the current user
        wish = models.WishList.objects.get(slug =slug , user=request.user)
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
def order_cart(request, slug):
    cart = models.Cart.objects.get(slug=slug)
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


#HOMEWORK 
@api_view(['GET'])
def category_list(request):
    categories = models.Category.objects.all()
    serializer = serializers.CategorySerializer(categories, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def category_detatil(request, slug):
    category = models.Category.objects.get(slug = slug)
    products = models.Product.objects.filter(category = category)
    cat_serializer = serializers.CategorySerializer(category)
    product_serializer = serializers.ProductSerializer(products, many = True)
    context = {
        'category': cat_serializer.data ,
        'related_products' : product_serializer.data
    }
    return Response (context)

@api_view(["GET"])
def product_list(request):
    products = models.Product.objects.all()
    serializer = serializers.ProductSerializer(products, many = True)
    return Response(serializer.data)

@api_view(["GET"])
def product_detail(request, slug):
    product = models.Product.objects.get(slug = slug)
    images = models.ProductImage.objects.filter(product_id = id)
    prod_serializer = serializers.ProductSerializer(product)
    image_serializer = serializers.ProductImageSerializer(images, many = True)
    context  = {
        'product': prod_serializer.data,
        'related_images': image_serializer.data
    }
    return Response(context)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def wishlist_create(request, slug):
    data = models.WishList.objects.filter(user = request.user, product__slug = slug).first()
    if data:
        return Response({'report':'wish for this product was already created'})
    else:
        new = models.WishList.objects.create(
            user = request.user,
            product = models.Product.objects.get(id = id)
        )
        serializer = serializers.WishlistSerializer(new)
        context = {
            'report': 'Created successfully',
            'wishlist': serializer.data
        }
        return Response(context)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def wishlist_delete(request, slug):
    data = models.WishList.objects.filter(user = request.user, product__slug = slug).first()
    if data:
        data.delete()
        return Response({'report': 'deleted successfully'})
    else:
        return Response({'report': 'there is no wishlist to delete'})



@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def reviewing(request, slug):

    """ bu funksiyada review yaratilmagan bo'lsa yaratadi, mavjud bo'lsa update qiladi. Review_CREATE, review_UPDATE"""

    data = models.ProductReview.objects.filter(product__slug = slug, user = request.user).first()
    if not data:
        if request.method == "POST":
            new = models.ProductReview.objects.create(
                user = request.user,
                product = models.Product.objects.get(id =id),
                mark = request.data.get('mark')
            )
            serializer = serializers.ProductReviewSerializer(new)
            context = {
                'report': 'created succesfully',
                'new_review' : serializer.data
            }
            return Response(context)
        else:
            return Response({'report': 'not POSTed yet',
                             'status': 'creation'})
    else:
        if request.method == 'POST':
            data.mark = request.data.get('mark')
            data.save()
            serializer = serializers.ProductReview(data)
            context = {
                'report': 'updated succesfully',
                'updated_review': serializer
            }
            return Response(context)
        
        else:
            return Response({'report': 'not POSTed yet',
                             'status': 'Updating session'})

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_active(request):
    data = models.Cart.objects.filter(user = request.user, is_active = True).first()
    
    if data:
        serializer = serializers.CartSerializer(data)
        return Response(serializer.data)
    else:
        return Response({"report": 'you do not have any active cart yet'})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_inactive(request):
    data = models.Cart.objects.filter(user = request.user, is_active = False)
    if data.first():
        serializer = serializers.CartSerializer(data, many = True)
        return Response(serializer.data)
    else:
        return Response({"report": 'you do not have any inactive cart yet'})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_update(request, slug):
    data = models.Cart.objects.filter(slug=slug)
    if data.first():
        cart = data.first()
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
        return Response ({'detail':'cart status updated succesfully'})
    else:
        return Response ({'detail':'cart status updated succesfully'})
    

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    cart = models.Cart.objects.filter(is_active = True).first()
    if cart:
        prodcuts = models.CartProduct.objects.filter(card = cart)
        cart_serializer = serializers.CartSerializer(cart)
        product_serializer = serializers.CartProductSerializer(prodcuts, many=True)
        context = {
            'cart' : cart_serializer.data,
            'related_products': product_serializer.data
        }
        return Response(context)
    else:
        return Response({'detail': 'there is no any cart to see the details'})

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_product(request, slug): #id -> product_id
    """ bu funksiyada cart_product yaratilmagan bo'lsa yaratadi, mavjud bo'lsa update qiladi. cart_product_CREATE, cart_product_UPDATE"""
    cart = models.Cart.objects.filter(user = request.user).first()
    if not cart:
        new_cart = models.Cart.objects.create(
            user = request.user
        )
        data = models.CartProduct.objects.create(
            card = new_cart,
            product = models.Product.objects.get(slug = slug),
            quantity = 1
        )
        serializer = serializers.CartProductSerializer(data)
        
        return Response({'detail':'cart and cart_product created successfully', 'new_cart_product' : serializer.data})
    else:
        expect = models.CartProduct.objects.filter(product_id = id, card = cart).first()
        if expect:
            expect.quantity+=1
            expect.save()
            serializer = serializers.CartProductSerializer(expect)
            return Response({'detail':'updated successfully', 'updated_cart_product' : serializer.data})
        else:
            data = models.CartProduct.objects.create(
                card= cart,
                product = models.Product.objects.get(id = id),
                quantity = 1
            )
            serializer = serializers.CartProductSerializer(data)
            return Response({'detail':'created successfully', 'new_cart_product' : serializer.data})

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_product_delete(request,slug): # id -> product_id
    cart = models.Cart.objects.filter(user = request.user, is_active = True).first()
    if cart:
        expect = models.CartProduct.objects.filter(card__is_active = True, product__slug = slug).first()
        print(expect)
        if expect:
            if expect.quantity > 1:
                expect.quantity-=1
                expect.save()
                serializer = serializers.CartProductSerializer(expect)
                return Response ({"detail": "Your cart-product's quantity reduced by one", "cart_product" : serializer.data})
            elif expect.quantity == 1:
                expect.delete()
                return Response ({'detail': 'cart-product deleted successfully'})

        else:
            return Response ({'detail': 'you do not have that cart_product to delete'})

    else:
        ({'detail': 'you do not have cart and cart_product to delete'})


@api_view(['GET'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username = username, password = password)
    if user:
        token, _ = Token.objects.get_or_create(user = user)
        data = {
            'token' : token.key
        }
    else:
        data = {
            'detail' : 'incorrect username or password'
        }
    return Response (data)

@api_view(['POST'])
def register(request):
    username = request.data['username']
    password = request.data['password']
    if not User.objects.filter(username = username):

        user = User.objects.create_user(
            username = username,
            password= password
        ) 
        token = Token.objects.create(user = user)
        return Response(
            {
                'username':username,
                'token': token.key
            }
        )
    else:
        return Response (
            {
                'detail': 'username is occupied'
            }
        )
    
@api_view(["POST", "GET"])
def find_cart(request, id):
    cart_products = models.CartProduct.objects.filter(card_id = id)
    cartproduct_serializer = serializers.CartProductSerializer(cart_products, many = True)
    return Response(cartproduct_serializer.data)

@api_view(["POST", "GET"])
def cart_status(request, id):
    cart = models.Cart.objects.get(id = id)
    if cart.status == 1:
        cart.status = 2
        cart.save()
        return Response({'detail': 'suceessfully changed'})
    else:
        return Response({'detail': 'cannot be changed'})

