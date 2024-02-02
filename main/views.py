from django.shortcuts import render, redirect
from . import models
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 


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
    context = {
        'products':products,
        'categorys':categorys
    }
    return render(request, 'index.html', context)

def filtered(request, id):
    products = models.Product.objects.filter(category_id = id)
    context = {

        'categorys': models.Category.objects.all(),
        'products': products
    }
    return render(request, 'categ/filtered.html', context)




def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    categorys = models.Category.objects.all()
    recomendation = models.Product.objects.filter(
        category_id=product.category.id).exclude(id=product.id)[:3]
    images = models.ProductImage.objects.filter(product_id=product.id)


    context = {
        'product':product,
        'categorys':categorys,
        'recomendation':recomendation,
        'images':images,
        'range':range(product.review)
    }
    return render(request, 'product/detail.html', context)


def carts(request):
    active = models.Cart.objects.filter(is_active=True, user=request.user)
    in_active = models.Cart.objects.filter(is_active=False, user=request.user)
    context = {
        'active':active,
        'in_active':in_active
    }
    return render(request, 'cart/carts.html', context)


def cart_detail(request, id):
    cart = models.Cart.objects.get(id=id)
    items = models.CartProduct.objects.filter(card=cart)
    context = {
        'cart':cart,
        'items':items
    }
    return render(request, 'cart/cart_detail.html', context)


def cart_detail_delete(request):
    item_id = request.GET['items_id']
    item = models.CartProduct.objects.get(id=item_id)
    cart_id = item.card.id
    item.delete()
    return redirect('main:cart_detail', cart_id)

def login_user(request):
    login_error = False
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,  password=password)
        if user:
            login(request, user)
            return redirect('main:index')
        else:
            login_error = "Incorrect username or password. Please try again."
    return render(request, 'login/login.html', {"login_error": login_error})


def regist(request):
    error = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not models.User.objects.filter(username = username):
            models.User.objects.create_user(
                username=username,
                password=password
            )
            
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('main:index')
        else:
            error = f"the username {username} already exists"
    return render(request, 'login/register.html', {'error': error})


def logout_user(request):
    logout(request)
    return redirect('main:login')

@login_required(login_url='main:login')
def create_cart(request, id):           #agar foydalanuvchida Cart bo'lmasa yoki u aktiv bo'lmasa yangi Cart yaratadi
    product = models.Product.objects.get(id = id)
    if models.Cart.objects.filter(user = request.user, is_active = True):
        return redirect('main:add_to_cart', id_product = product.id, id_user = request.user.id)
    else:
        models.Cart.objects.create(
            user = request.user
        )
        return redirect ('main:add_to_cart', id_product = product.id, id_user = request.user)

def add_to_cart(request, id_product, id_user):
    product = models.Product.objects.get(id = id_product)
    cart = models.Cart.objects.get(user_id = id_user, is_active = True)
    previous_url = request.META.get('HTTP_REFERER')
    if models.CartProduct.objects.filter(product_id= id_product):
        data = models.CartProduct.objects.get(product_id = id_product)
        data.quantity +=1
        data.save()
        return redirect(previous_url)
    else:
        models.CartProduct.objects.create(
            product = product,
            card = cart,
            )
        return redirect(previous_url)


