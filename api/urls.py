from . import views
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('', views.index, name='index'),
    path('filtered/<int:id>', views.filtered, name = 'filtered'),
    # path('product/<int:id>', views.product_detail, name='product_detail'),
    path('carts', views.carts, name='carts'),
    path('cart/<int:id>/', views.cart_detail, name='cart_detail'),
    # path('cart/detail/delete/', views.cart_detail_delete, name='cart_detail_delete'),

    path('login', views.login_user, name = 'login') ,
    path('register', views.regist, name = 'register'),
    path('logout,', views.logout_user, name='logout'),

    path('create-cart/<int:id>/', views.create_cart, name = 'create_cart'),
    path('add-to-cart/<int:id_product>/<int:id_user>', views.add_to_cart, name='add_to_cart'),
    #wishlist
    path('wishlist', views.wishlist, name='wishlist'),
    path('add_wish/<int:id>', views.add_wish, name = 'add_wish'),
    path('delete-wish/<int:id>', views.delete_wish, name = 'delete_wish'),

    path('settings', views.user_update, name = 'user_update'),
    path('order/<int:id>', views.order_cart, name = 'order'),


    #HOMEWORK
    #category
    path('category-list', views.category_list, name = 'cat_list'),
    path('category-detail/<int:id>', views.category_detatil, name = 'cat_det'),
    #product
    path('product-list', views.product_list, name = 'prod_list'),
    path('product-detail/<int:id>', views.product_detail, name = 'prod_det'),
    #wish
    path('wish-create/<int:id>', views.wishlist_create, name = 'wish_create'),
    path('wish-delete/<int:id>', views.wishlist_delete, name = 'wish_delete'),
    #review
    path('reviewing/<int:id>', views.reviewing, name = 'reviewing'), #review yaratish va o'zgartirish uchun
    #cart
    path('cart-active/', views.cart_active, name = 'cart_active'),
    path('cart-inactive/', views.cart_inactive, name = 'cart_inactive'),
    path('cart-update/<int:id>', views.cart_update, name = 'cart_update'),
    path('cart-detail/', views.cart_detail, name = 'cart_detail'),
    #cart-product
    path('cart-product/<int:id>', views.cart_product, name = 'cart_product'), #cart_product yaratish va o'zgartirish uchun
    path('cart-product-delete/<int:id>', views.cart_product_delete, name = 'cart_product_delete')
]