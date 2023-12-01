from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomAccessPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        # return request.user and request.user.is_superuser
        return request.user and request.user.groups.filter(name='Manager').exists()