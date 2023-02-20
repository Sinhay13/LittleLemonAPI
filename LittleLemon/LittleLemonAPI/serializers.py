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
