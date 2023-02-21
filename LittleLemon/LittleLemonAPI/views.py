
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

# group management: "Manager"


from .serializers import UserIdSerializer
class GroupManagerListView(generics.ListCreateAPIView):
    serializer_class = UserIdSerializer

    def get_queryset(self):
        managers_group = Group.objects.get(name='Manager')
        managers = managers_group.user_set.all()
        for i, manager in enumerate(managers):
            manager.id = i + 1
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

class GroupManagerUserView(generics.DestroyAPIView):
    lookup_field = 'id'

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied()

    def get_queryset(self):
        managers_group = Group.objects.get(name='Manager')
        return managers_group.user_set.all()

    def delete(self, request, *args, **kwargs):
        manager_id = kwargs.get('manager_id')
        user = get_object_or_404(User, id=manager_id)
        managers_group = Group.objects.get(name='Manager')
        managers_group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)



#____________________________________________________________________________________________________#

# group management: "Delivery"

class GroupDeliveryListView(generics.ListCreateAPIView):
    serializer_class = UserIdSerializer

    def get_queryset(self):
        crews_group = Group.objects.get(name='Delivery')
        crews = crews_group.user_set.all()
        for i, crew in enumerate(crews):
            crew.id = i + 1
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

class GroupDeliveryUserView(generics.DestroyAPIView):
    lookup_field = 'crew_id'

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied()

    def get_queryset(self):
        crews_group = Group.objects.get(name='Delivery')
        return crews_group.user_set.all()

    def delete(self, request, *args, **kwargs):
        crews_id = kwargs.get('crews_id')
        user = get_object_or_404(User, id=crews_id)
        managers_group = Group.objects.get(name='Delivery')
        managers_group.user_set.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

#____________________________________________________________________________________________________#



# trouve le probleme pourquoi je n'arrive pas a faire la delete et verifier que les message d'erreur sois bien les meme que dans l'enoncer 

