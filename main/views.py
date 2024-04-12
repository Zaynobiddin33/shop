from django.contrib import messages
from django.shortcuts import render, redirect
from . import models
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect


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
        'categorys':categorys,
        'wished': models.WishList.objects.all()
    }
    return render(request, 'index.html', context)

def filtered(request, slug):
    products = models.Product.objects.filter(category__slug = slug)
    context = {

        'categorys': models.Category.objects.all(),
        'products': products
    }
    return render(request, 'categ/filtered.html', context)




def product_detail(request, slug ) :
    product = models.Product.objects.get(slug = slug) 
    categorys = models.Category.objects.all()
    recomendation = models.Product.objects.filter(
        category_id=product.category.id).exclude(id=product.id)[:3]
    images = models.ProductImage.objects.filter(product_id=product.id)
    if models.WishList.objects.filter(product = product):
        is_wished = True
    else:
        is_wished = False


    context = {
        'product':product,
        'categorys':categorys,
        'recomendation':recomendation,
        'images':images,
        'is_wished': is_wished
    }
    if request.method == 'POST':
        user = request.user
        mark = request.POST['rate']
        product = models.Product.objects.get(id = request.POST['product_id'])
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
    return render(request, 'product/detail.html', context)


def carts(request):
    active = models.Cart.objects.filter(is_active=True, user=request.user)
    in_active = models.Cart.objects.filter(is_active=False, user=request.user).order_by('-id')
    context = {
        'active':active,
        'in_active':in_active,
        'categorys': models.Category.objects.all(),
    }
    return render(request, 'cart/carts.html', context)


def cart_detail(request, slug):
    cart = models.Cart.objects.get(slug=slug)
    items = models.CartProduct.objects.filter(card = cart)
    context = {
        'cart':cart,
        'items':items,
        'categorys': models.Category.objects.all(),
    }
    return render(request, 'cart/cart_detail.html', context)


def cart_detail_delete(request):
    item_id = request.GET['items_id']
    item = models.CartProduct.objects.get(id=item_id)
    cart_id = item.card.id
    item.delete()
    previous_page = request.META.get('HTTP_REFERER')

    # Redirect back to the previous page
    return HttpResponseRedirect(previous_page)

@csrf_exempt
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


@csrf_exempt
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
    return redirect('main:index')

@login_required(login_url='main:login')
def create_cart(request, slug):           #agar foydalanuvchida Cart bo'lmasa yoki u aktiv bo'lmasa yangi Cart yaratadi
    product = models.Product.objects.get(slug = slug)
    if models.Cart.objects.filter(user = request.user, is_active = True).first():
        return redirect('main:add_to_cart', id_product = product.id, id_user = request.user.id)
    else:
        models.Cart.objects.create(
            user = request.user
        )
        return redirect ('main:add_to_cart', id_product = product.id, id_user = request.user.id)

def add_to_cart(request, id_product, id_user):
    product = models.Product.objects.get(id = id_product)
    cart = models.Cart.objects.get(user_id = id_user, is_active = True)
    previous_url = request.META.get('HTTP_REFERER')
    if models.CartProduct.objects.filter(product_id = id_product, card = cart).first():
        data = models.CartProduct.objects.get(product_id = id_product, card = cart)
        data.quantity +=1
        data.save()
        return redirect(previous_url)
    else:
        models.CartProduct.objects.create(
            product = product,
            card = cart,
            )
        return redirect(previous_url)
    
def wishlist(request):
    items = models.WishList.objects.filter(user = request.user)
    context = {
        'items': items,
        'categorys': models.Category.objects.all()
    }
    return render(request, 'wish/list.html', context)

def add_wish(request,slug):
    if not request.user.is_authenticated:
        return redirect ('main:login')
    previous_url = request.META.get('HTTP_REFERER')
    product = models.Product.objects.get(slug = slug)
    models.WishList.objects.create(
        product = product,
        user = request.user
    )
    return redirect (previous_url)

def delete_wish(request, slug):
    if request.META.get('HTTP_REFERER').startswith('http://127.0.0.1:8000/product'):
        product = models.Product.objects.get(slug = slug)
        models.WishList.objects.get(product = product).delete()
    else:
        models.WishList.objects.get(slug = slug).delete()

    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)


def user_update(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            new_username = request.POST.get('username')
            new_password = request.POST.get('password')

            if models.User.objects.filter(username=new_username).exclude(pk=request.user.pk).exists():
                messages.error(request, 'Username is already taken.')
            else:
                user = request.user
                user.username = new_username
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('main:index')
    
    return render(request, 'user/update.html')

def order_cart(request, slug):
    cart = models.Cart.objects.get(slug=slug)
    print('q')
    objects = models.CartProduct.objects.filter(card = cart)
    print('2')
    for obj in objects:
        prod = models.Product.objects.get(id = obj.product.id)
        new_quant = obj.product.quantity-obj.quantity

        if new_quant>=0:
            prod.quantity = new_quant
            prod.save()
            data = models.Overall.objects.get(product = obj.product)
            data.all_outcome +=obj.quantity
            models.ProductOut.objects.create(
                product = prod,
                amount = obj.quantity
            )
            print('created')
        else:
            print('if2')
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

    return redirect(f'https://t.me/numi_store_bot?start={cart.id}')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        models.Contact.objects.create(
            name = name,
            email = email,
            message = message
        )
        previous_page = request.META.get('HTTP_REFERER')

        # Redirect back to the previous page
        return redirect('main:index')
    return render(request, 'contact.html')
