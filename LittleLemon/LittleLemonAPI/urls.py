
# urls.py in the app directory
from django.urls import path, include
from .views import CategoryList, CategoryDetail, MenuItemList, MenuItemDetail, CartList, CartDetail, OrderList, OrderDetail

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('menu-items/', MenuItemList.as_view(), name='menu-item-list'),
    path('menu-items/<int:pk>/', MenuItemDetail.as_view(), name='menu-item-detail'),
    path('carts/', CartList.as_view(), name='cart-list'),
    path('carts/<int:pk>/', CartDetail.as_view(), name='cart-detail'),
    path('orders/', OrderList.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
]