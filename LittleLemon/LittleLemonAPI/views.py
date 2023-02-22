
#Import: 
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

# Category :
from .models import Category
from .serializers import CategorySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# to check acces : 
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if self.request.method not in ['GET', 'HEAD', 'OPTIONS']:
            if not request.user.groups.filter(name='Manager').exists():
                raise PermissionDenied()
# to personalize response :
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({'message': '403 - Unauthorized '}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    
 # to check acces : 
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if self.request.method not in ['GET', 'HEAD', 'OPTIONS']:
            if not request.user.groups.filter(name='Manager').exists():
                raise PermissionDenied()
# to personalize response :
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({'message': '403 - Unauthorized '}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)
    
    def retrieve(self, request, id=None, *args, **kwargs):
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            raise NotFound("Category not found")
        serializer = CategorySerializer(category)
        return Response(serializer.data)
#_____________________________________________________________________________________________#
# Menu-items: 
from .models import MenuItem
from .serializers import MenuItemSerializer

class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    # to check acces : 
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if self.request.method not in ['GET', 'HEAD', 'OPTIONS']:
            if not request.user.groups.filter(name='Manager').exists():
                raise PermissionDenied()
    # to personalize response :
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({'message': '403 - Unauthorized '}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)

class MenuItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    lookup_field = 'pk'
    
    # to check acces : 
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if self.request.method not in ['GET', 'HEAD', 'OPTIONS']:
            if not request.user.groups.filter(name='Manager').exists():
                raise PermissionDenied()
    # to personalize response :
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({'message': '403 - Unauthorized '}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)

#_________________________________________________________________________________________________#

from .serializers import UserSerializer
# manager managment :
class GroupManagerListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        managers_group = Group.objects.get(name='Manager')
        managers = managers_group.user_set.all()
        return managers

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            managers_group = Group.objects.get(name='Manager')
            managers_group.user_set.add(user)
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GroupManagerUserView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        managers_group = Group.objects.get(name='Manager')
        managers_group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
#____________________________________________________________________________________________________#

# delivery managment :
class GroupDeliveryListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        crews_group = Group.objects.get(name='Delivery')
        crews= crews_group.user_set.all()
        return crews

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            crews_group = Group.objects.get(name='Delivery')
            crews_group.user_set.add(user)
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GroupDeliveryUserView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = User.objects.filter(groups__name='Delivery')
    serializer_class = UserSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        crews_group = Group.objects.get(name='Delivery')
        crews_group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
#____________________________________________________________________________________________________#


# Cart: 
from .models import Cart
from .serializers import CartSerializer
from rest_framework.exceptions import ValidationError

class CartListView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#______________________________________________________________________________________________________#
