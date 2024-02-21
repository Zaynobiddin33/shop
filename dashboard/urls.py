from . import views
from django.urls import path

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dash'),
    path('product-list', views.products),
    path('product-create', views.product_create),

    path('category-create', views.category_create, name='category_create'),
    path('category-list', views.category_list, name='category_list'),
    path('category-update/<str:slug>', views.category_update, name='category_update'),
    path('category-delete/<str:slug>', views.category_delete, name='category_delete'),

    path('product-list', views.products, name='products'),
    path('product-create', views.product_create, name = 'product_create'),
    path('product-update/<str:slug>', views.product_update, name='product_update'),
    path('product-delate/<str:slug>', views.product_delete, name='product_delete'),
    path('image-delete/<str:slug>', views.image_delete, name='image_delete'),

    path('add-admin', views.add_admin, name='add_admin'),
    path('list-admin', views.admins, name='admins'),
    path('delete-admin/<str:slug>', views.delete_admin, name='delete_admin'),

    path('income',views.income, name='income'),
    path('income-list', views.list_income, name = 'list_enter'),
    path('enter-update/<str:slug>/', views.update_income, name='update_enter'),
    path('enter-delete/<str:slug>/', views.delete_income, name='delete_enter'),
    path('income-excel', views.income_excel, name='excel'),
    path('overall', views.income_outcome, name = 'overall'),
    path('overall-excel', views.overall_excel, name='overall_excel'),
    path("input-excel", views.excel_input, name='excel_input'),
    path('detail/<str:slug>', views.product_detail , name = 'detail')


]