
# urls.py in the app directory
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('users/', RedirectView.as_view(url='/auth/users')), # to create a user
]