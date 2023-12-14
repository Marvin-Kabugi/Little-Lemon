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
    # user = UserSerializer()
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        # write_only=True,
        default=serializers.CurrentUserDefault()
    )
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'quantity', 'unit_price', 'price', 'user', 'menuitem', 'menuitem_id']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    delivery_crew = UserSerializer(read_only=True)
    delivery_crew_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'date', 'user', 'delivery_crew', 'order_items', 'user_id', 'delivery_crew_id']

    def get_order_items(self, obj):
        items = obj.order_items.all()
        return OrderItemSerializer(items, many=True, read_only=True).data
    

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        update_fields=['status']

        if user.groups.filter(name='Delivery Crew').exists():
            for item in validated_data:
                if item not in update_fields:
                    raise serializers.ValidationError('Delivery crew can\'t update this field')
            instance.status = validated_data.get('status', instance.status)
        else:
            for item in validated_data:
                if hasattr(instance, item):
                    setattr(instance, item, validated_data[item])
        instance.save()

        return instance

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(write_only=True)
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price', 'price', 'order', 'menuitem', 'menuitem_id']