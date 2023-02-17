from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound




# Category :
from .models import Category
from .serializers import CategorySerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def retrieve(self, request, id=None, *args, **kwargs):
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            raise NotFound("Category not found")
        serializer = CategorySerializer(category)
        return Response(serializer.data)
#_____________________________________________________________________________________________#
# Menu-items: 

# A faire ici

#_________________________________________________________________________________________________#