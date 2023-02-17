
from django.urls import path, include
from django.views.generic.base import RedirectView
#from . import views
from .views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView

urlpatterns = [
    path('users/', RedirectView.as_view(url='/auth/register')), # to create a user
    path('users/me/', RedirectView.as_view(url='/auth/users/me')), # to see own data
    #path('menu-items/', views.menu_items, name='menu-items'),
    #path('menu-items/<int:menuitem>/', views.menu_items, name='single'),
    path('category/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category/<int:id>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),
]