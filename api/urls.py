from . import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('filtered/<str:slug>', views.filtered, name = 'filtered'),
    # path('product/<str:slug>', views.product_detail, name='product_detail'),
    path('carts', views.carts, name='carts'),
    path('cart/<str:slug>/', views.cart_detail, name='cart_detail'),
    # path('cart/detail/delete/', views.cart_detail_delete, name='cart_detail_delete'),

    path('login', views.login, name = 'login') ,
    path('register', views.register, name = 'register'),
    path('logout,', views.logout_user, name='logout'),

    path('create-cart/<str:slug>/', views.create_cart, name = 'create_cart'),
    path('add-to-cart/<int:id_product>/<int:id_user>', views.add_to_cart, name='add_to_cart'),
    #wishlist
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_wish/<str:slug>', views.add_wish, name = 'add_wish'),
    path('delete-wish/<str:slug>', views.delete_wish, name = 'delete_wish'),

    path('settings', views.user_update, name = 'user_update'),
    path('order/<str:slug>', views.order_cart, name = 'order'),


    #HOMEWORK
    #category
    path('category-list', views.category_list, name = 'cat_list'),
    path('category-detail/<str:slug>', views.category_detatil, name = 'cat_det'),
    #product
    path('product-list', views.product_list, name = 'prod_list'),
    path('product-detail/<str:slug>', views.product_detail, name = 'prod_det'),
    #wish
    path('wish-create/<str:slug>', views.wishlist_create, name = 'wish_create'),
    path('wish-delete/<str:slug>', views.wishlist_delete, name = 'wish_delete'),
    #review
    path('reviewing/<str:slug>', views.reviewing, name = 'reviewing'), #review yaratish va o'zgartirish uchun
    #cart
    path('cart-active/', views.cart_active, name = 'cart_active'),
    path('cart-inactive/', views.cart_inactive, name = 'cart_inactive'),
    path('cart-update/<str:slug>', views.cart_update, name = 'cart_update'),
    path('cart-detail/', views.cart_detail, name = 'cart_detail'),
    #cart-product
    path('cart-product/<str:slug>', views.cart_product, name = 'cart_product'), #cart_product yaratish va o'zgartirish uchun
    path('cart-product-delete/<str:slug>', views.cart_product_delete, name = 'cart_product_delete')
]