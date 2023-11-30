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