from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import Group

class CustomAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        # return request.user and request.user.is_superuser
        return request.user and request.user.groups.filter(name='Manager').exists()
    

class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='Manager').exists()
    

class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        manager_group = Group.objects.get(name='Manager')
        delivery_group = Group.objects.get(name='Delivery Crew') 
        check = manager_group in request.user.groups.all() or delivery_group in request.user.groups.all()
        return not check
    

