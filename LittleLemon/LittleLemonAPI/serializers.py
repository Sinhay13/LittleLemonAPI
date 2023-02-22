from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem

#Category: 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
#________________________________________________________________#

#Menu-Items:
class MenuItemSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True)
    category_id=serializers.SlugField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', "category_id"]

#_____________________________________________________________________#

# for users management: 
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Cart :

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.SlugRelatedField(slug_field='title', queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=100)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'menuitem', 'quantity', 'unit_price', 'price')

    def validate(self, data):
        menuitem = data['menuitem']
        quantity = data['quantity']
        data['unit_price'] = menuitem.price
        data['price'] = menuitem.price * quantity
        return data

#______________________________________________________________________#