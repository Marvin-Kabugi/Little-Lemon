from functools import reduce
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import  generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, UserSerializer, UserGroupSerializer
from .models import Category, MenuItem, Cart, Order, OrderItem
from .permissions import CustomAccessPermission, ManagerPermission, CustomerPermission, DeliveryCrewPermission
# Create your views here.


# Class based view for managing listing and creation of Menu Items 
class MenuItemsList(APIView):
    permission_classes = [CustomAccessPermission]

    def get(self, request, format=None):
        menuitems = MenuItem.objects.all()
        serializer = MenuItemSerializer(menuitems, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Class based view for managing listing, updating and deleting a single Menu Item
class MenuItemsDetail(APIView):
    permission_classes = [CustomAccessPermission]

    def get_object(self, pk):
        try:
            return MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return None

    def get(self, request, pk, format = None):
        menu_item = self.get_object(pk)
        if menu_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND) 
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def patch(self, request, pk, format = None):
        menu_item = self.get_object(pk)
        if menu_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, pk, format = None):
        menu_item = self.get_object(pk)
        if menu_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MenuItemSerializer(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        menu_item = self.get_object(pk)
        if menu_item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        menu_item.delete()
        return Response(status=status.HTTP_200_OK)
    

# Class based view for managing User groups. Creation and Listing of.
class UserGroupList(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request, format=None):
        users = User.objects.filter(groups__name="Manager")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, format=None):
        '''
            Payload Format:
            {
                "id": <int: id>,
                "username": <str: username>
            }
        '''
        group = Group.objects.get(name="Manager")
        serializer = UserGroupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user= User.objects.get(username=serializer.validated_data.get('username'))
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            user.groups.add(group)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

class UserGroupDetail(APIView):
    permission_classes = [ManagerPermission]

    def delete(self, request, pk, format=None):
        group = Group.objects.get(name="Manager")
        
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user.groups.remove(group)
        return Response(status=status.HTTP_200_OK)
    

class DeliveryGroupList(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request, format=None):
        users = User.objects.filter(groups__name="Delivery Crew")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, format=None):
        '''
            Payload Format:
            {
                "id": <int: id>,
                "username": <str: username>
            }
        '''
        group = Group.objects.get(name="Delivery Crew")
        serializer = UserGroupSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(username=serializer.validated_data.get('username'))
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            user.groups.add(group)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeliveryGroupDetail(APIView):
    permission_classes = [ManagerPermission]

    def delete(self, request, pk, format=None):
        group = Group.objects.get(name="Delivery Crew")
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        user.groups.remove(group)
        return Response(status=status.HTTP_200_OK)
        

class CartList(APIView):
    permission_classes = [permissions.IsAuthenticated, CustomerPermission]

    def get(self, request, format=None):
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        user_menu_items = Cart.objects.filter(user=user)
        menuitems = [item.menuitem for item in user_menu_items]
        # print(menuitems)
        # serializer = CartSerializer(user_menu_items, many=True)
        serializer = MenuItemSerializer(menuitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        username = request.user.username

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        Cart.objects.filter(user=user).delete()
        return Response({'message': 'Deleted Cart'}, status=status.HTTP_200_OK)
    


class OrderList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if ManagerPermission().has_permission(request, self):
            orders = Order.objects.all()
        elif DeliveryCrewPermission().has_permission(request, self):
            orders = Order.objects.filter(delivery_crew=request.user.id)
        else:
            orders = Order.objects.filter(user=request.user.id)
        print(orders)
        print(request.user, ':', request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            print(order)
            menu_items = CartList().get(request).data
            print(menu_items)
            for item in menu_items:
                cart = Cart.objects.get(user=request.user, menuitem=item.get('id'))
                print('done')
                OrderItem.objects.create(
                    order=order,
                    menuitem_id=item.get('id'),
                    quantity=cart.quantity,
                    unit_price=cart.unit_price,
                    price=cart.price
                )

            order.total = reduce(lambda x, y: x + y, [order.price for order in OrderItem.objects.filter(order=order)])
            order.save()
            CartList().delete(request)
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None
        
        
    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        if order is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if CustomerPermission().has_object_permission(request, self, order):
            serializer = OrderSerializer(order)
            return Response(serializer.data['order_items'], status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        if ManagerPermission().has_permission(request, self): 
            order = self.get_object(pk)

            if order is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(order, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def patch (self, request, pk, format=None):
        if ManagerPermission().has_permission(request, self) or DeliveryCrewPermission().has_permission(request, self):
            order = self.get_object(pk)

            if order is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = OrderSerializer(order, data=request.data, partial=True, context={"request": request})

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        if ManagerPermission().has_permission(request, self):
            order = self.get_object(pk)
            order.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)



    