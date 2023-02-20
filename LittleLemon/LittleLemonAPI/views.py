
#Import: 
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import MenuItem
from .serializers import MenuItemSerializer



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
    #permission_classes = [IsAuthenticated]

class MenuItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    lookup_field = 'pk'
    #permission_classes = [IsAuthenticated]

#_________________________________________________________________________________________________#