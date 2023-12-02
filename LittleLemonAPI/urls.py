from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('menu-items', views.MenuItemsList.as_view(), name='menu-list'),
    path('menu-items/<int:pk>', views.MenuItemsDetail.as_view(), name='menu-item-detail'),
    path('groups/managers/users', views.UserGroupList.as_view(), name='user-group-list'),
    path('groups/managers/users/<int:pk>', views.UserGroupDetail.as_view(), name='user-individual'),
    path('groups/delivery-crew/users', views.DeliveryGroupList.as_view(), name='crew-delivery-list'),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryGroupDetail.as_view(), name='crew-individual'),
    path('cart/menu-items', views.CartList.as_view(), name='cart')
]

urlpatterns = format_suffix_patterns(urlpatterns)
