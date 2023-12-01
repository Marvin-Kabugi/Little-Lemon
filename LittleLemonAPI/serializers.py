from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Order, OrderItem, Cart


class UserGroupSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username']

    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only = True)
    
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(),
    #     many=False
    # )

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

    # overide to_representation 
    # def to_representation(self, instance):
        # Use the nested CategorySerializer for read operations
        # self.fields['category'] = CategorySerializer()
        # return super(MenuItemSerializer, self).to_representation(instance)

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    menuitem = MenuItemSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'quantity', 'unit_price', 'price', 'user', 'menuitem']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    delivery_crew = UserSerializer()
    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'date', 'user', 'delivery_crew']


class OrderItemSerializer(serializers.ModelSerializer):
    order = UserSerializer()
    menuitem = MenuItemSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price', 'price', 'order', 'menuitem']