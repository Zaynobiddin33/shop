from . import views
from django.urls import path

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dash'),
    path('product-list', views.products),
    path('product-create', views.product_create),

    path('category-create', views.category_create, name='category_create'),
    path('category-list', views.category_list, name='category_list'),
    path('category-update/<int:id>', views.category_update, name='category_update'),
    path('category-delete/<int:id>', views.category_delete, name='category_delete'),

    path('product-list', views.products, name='products'),
    path('product-create', views.product_create, name = 'product_create'),
    path('product-update/<int:id>', views.product_update, name='product_update'),
    path('product-delate/<int:id>', views.product_delete, name='product_delete'),
    path('image-delete/<int:id>', views.image_delete, name='image_delete'),

]