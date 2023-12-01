from django.shortcuts import render
from rest_framework import  generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .models import Category, MenuItem, Cart, Order, OrderItem
from .permissions import CustomAccessPermission
# Create your views here.

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
    

class MenuItemsDetail(APIView):
    permission_classes = [CustomAccessPermission]

    def get_object(self, pk):
        try:
            return MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item does not exist'},status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format = None):
        menu_item = self.get_object(pk)
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def patch(self, request, pk, format = None):
        menu_item = self.get_object(pk)
        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self, request, pk, format = None):
        menu_item = self.get_object(pk)
        serializer = MenuItemSerializer(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        menu_item = self.get_object(pk)
        menu_item.delete()
        return Response(status=status.HTTP_200_OK)