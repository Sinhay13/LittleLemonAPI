
from django.urls import path, include
from django.views.generic.base import RedirectView
from .views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView, MenuItemListCreateView, MenuItemRetrieveUpdateDestroyView, GroupManagerListView, GroupManagerUserView,GroupDeliveryListView, GroupDeliveryUserView , CartListView


urlpatterns = [
    path('users/', RedirectView.as_view(url='/auth/register')), # to create a user
    path('users/me/', RedirectView.as_view(url='/auth/users/me')), # to see own data
	path('menu-items/', MenuItemListCreateView.as_view(), name='menu_items_list_create'),
    path('menu-items/<int:pk>', MenuItemRetrieveUpdateDestroyView.as_view(), name='menu_items_retrieve_update_destroy'),
    path('category/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/<int:id>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
    path('groups/manager/users/', GroupManagerListView.as_view(), name='manager-users'),
    path('groups/manager/users/<int:id>/', GroupManagerUserView.as_view(), name='user-detail'),
    path('groups/delivery-crew/users/', GroupDeliveryListView.as_view(), name='delivery-users'),
    path('groups/delivery-crew/users/<int:id>/', GroupDeliveryUserView.as_view(), name='crew-detail'),
    path('cart/menu-items/', CartListView.as_view(), name='cart-list-create-delete'),



]