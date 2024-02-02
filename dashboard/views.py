from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from main.models import *


def dashboard(request):
    categorys =  Category.objects.all()
    products = Product.objects.all()
    users = User.objects.all()
    numusers = User.objects.all().count()
    numproducts = Product.objects.all().count()
    numcategories = Category.objects.all().count()
    context = {
        'categorys':categorys,
        'products':products,
        'users':users,
        'numusers':numusers,
        'numproducts':numproducts,
        'numcategories':numcategories
    }
    return render(request, 'dashboard/index.html', context)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category/list.html', {'categories':categories})


def category_detail(request, id):
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category, is_active=True)
    context = {
        'category':category,
        'products':products
    }
    return render(request, 'category/list.html', context)


def category_update(request, id):
    category = Category.objects.get(id=id)
    category.name = request.POST['name']
    category.save()

    return redirect('category_detail', {'category':category})


def category_delete(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('dashboard:category_list')

def category_create(request):
    if request.method == 'POST':
        Category.objects.create(
            name = request.POST['name']
        )
    return render(request, 'dashboard/category/create.html')



# products

def products(request):
    products = Product.objects.all()
    return render(request, 'dashboard/products/list.html',{'products':products})


def product_create(request):
    categorys = Category.objects.all()
    context = {
        'categorys':categorys
    }
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        quantity = request.POST['quantity']
        price = request.POST['price']
        currency = request.POST['currency']
        baner_image = request.FILES['baner_image']
        category_id = request.POST['category_id']
        images = request.FILES.getlist('images')
        product = Product.objects.create(
            name=name,
            description = description,
            quantity=quantity,
            price=price,
            currency=currency,
            baner_image=baner_image,
            category_id=category_id
        )
        for image in images:
            ProductImage.objects.create(
                image=image,
                product=product
            
            )

    return render(request, 'dashboard/products/create.html', context)

def product_update(request, id):
    product = Product.objects.get(id = id)
    images = ProductImage.objects.filter(product = product)
    context = {
        'product':product,
        'categorys':Category.objects.all(),
        'images': images
    }
    if request.method == "POST":
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.quantity = request.POST['quantity']
        product.price = request.POST['price']
        product.currency = request.POST['currency']
        try:
            product.baner_image = request.FILES['baner_image']
        except:
            pass
        product.category_id = request.POST['category_id']
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(
                image=image,
                product=product
            
            )
        product.save()
    return render (request, 'dashboard/products/update.html', context)

def product_delete(request, id):
    Product.objects.get(id = id).delete()
    return redirect('dashboard:products')

def image_delete(request, id):
    ProductImage.objects.get(id = id).delete()
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url )