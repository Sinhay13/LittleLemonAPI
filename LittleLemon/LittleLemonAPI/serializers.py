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
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=100)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    menuitem_name = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'menuitem', 'menuitem_name', 'quantity', 'unit_price', 'price')

    def get_menuitem_name(self, obj):
        return obj.menuitem.title

    def validate(self, data):
        menuitem = data['menuitem']
        quantity = data['quantity']
        data['unit_price'] = menuitem.price
        data['price'] = menuitem.price * quantity
        return data




#______________________________________________________________________#

# Orders: 

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('menuitem', 'quantity', 'unit_price', 'price')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.delivery_crew = validated_data.get('delivery_crew', instance.delivery_crew)
        instance.status = validated_data.get('status', instance.status)
        instance.total = validated_data.get('total', instance.total)
        instance.save()

        items_data = validated_data.get('items')
        if items_data:
            instance.orderitem_set.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
