from . import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('filtered/<int:id>', views.filtered, name = 'filtered'),
    path('product/<int:id>', views.product_detail, name='product_detail'),
    path('carts', views.carts, name='carts'),
    path('cart/<int:id>/', views.cart_detail, name='cart_detail'),
    path('cart/detail/delete/', views.cart_detail_delete, name='cart_detail_delete'),

    path('login', views.login_user, name = 'login') ,
    path('register', views.regist, name = 'register'),
    path('logout,', views.logout_user, name='logout'),

    path('create-cart/<int:id>/', views.create_cart, name = 'create_cart'),
    path('add-to-cart/<int:id_product>/<int:id_user>', views.add_to_cart, name='add_to_cart')
]