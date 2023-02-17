
# urls.py in the app directory
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('users/', RedirectView.as_view(url='/auth/register')), # to create a user
    path('users/me/', RedirectView.as_view(url='/auth/users/me')), # to see own data
   
]